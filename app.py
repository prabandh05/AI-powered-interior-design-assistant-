import os
import json
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from models import db, User
from auth_utils import encode_token, token_required
from dotenv import load_dotenv
from services.pipeline import InteriorDesignPipeline
from models import DesignHistory

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'users.db')
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "indian_interior_v2.json")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(os.path.dirname(DB_PATH)):
    os.makedirs(os.path.dirname(DB_PATH))

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key-for-dev')

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)

# Load dataset and initialize pipeline
with open(DATASET_PATH) as f:
    dataset = json.load(f)
pipeline = InteriorDesignPipeline(dataset)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return jsonify({"message": "Welcome to AI Interior Design Assistant API"})

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'images'), filename)

# --- Authentication Routes ---

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password') or not data.get('email') or not data.get('name'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'message': 'Username already exists'}), 400
        
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
    new_user = User(
        name=data.get('name'),
        username=data.get('username'),
        email=data.get('email'),
        password_hash=hashed_password,
        location=data.get('location', ''),
        is_admin=data.get('is_admin', False) # For hackathon convenience
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and bcrypt.check_password_hash(user.password_hash, data.get('password')):
        token = encode_token(user.id)
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'is_admin': user.is_admin,
            'name': user.name
        }), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user_id):
    return jsonify({'message': 'Successfully logged out'}), 200

# --- Core AI Interior Routes ---

@app.route("/generate-design", methods=["POST"])
# @token_required 
def generate_design():
    # Attempt to get user_id from token if available (semi-protected)
    auth_header = request.headers.get('Authorization')
    current_user_id = None
    if auth_header:
        # Simple extraction for history tracking, not strictly enforced for the generation itself
        from auth_utils import decode_token
        try:
            token = auth_header.split(" ")[1]
            current_user_id = decode_token(token)
        except:
            pass

    # Handle both JSON and Multipart data
    if request.is_json:
        user_input = request.json
    else:
        # Handle multipart/form-data
        user_input = {
            "description_text": request.form.get("description_text"),
            "theme": request.form.get("theme"),
            "budget": request.form.get("budget"),
        }
        
        # Check if previous_scene_data is present (for iterations)
        prev_data = request.form.get("previous_scene_data")
        if prev_data:
            user_input["previous_scene_data"] = json.loads(prev_data)
            
        file = request.files.get("image")
        if file and file.filename != "":
            filename = f"upload_{uuid.uuid4().hex[:8]}_{file.filename}"
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(image_path)
            user_input["image_path"] = image_path

    if not user_input:
        return jsonify({"status": "error", "message": "No input provided"}), 400
        
    result = pipeline.run(user_input)

    # Save to history if logged in
    if current_user_id and result.get("status") == "success":
        try:
            history = DesignHistory(
                user_id=current_user_id,
                theme=result["design_strategy"].get("theme", ""),
                space_type=result["design_strategy"].get("space_type", ""),
                budget=int(user_input.get("budget", 0)),
                total_cost=result["procurement"]["comparison_plans"][0].get("total_cost", 0) if result["procurement"]["comparison_plans"] else 0,
                selected_plan=result["procurement"]["comparison_plans"][0].get("plan_name", "") if result["procurement"]["comparison_plans"] else "Generic",
                image_url=result["visuals"]["image_links"][0] if result["visuals"]["image_links"] else ""
            )
            db.session.add(history)
            db.session.commit()
        except Exception as e:
            print(f"Error saving history: {e}")

    return jsonify(result)

@app.route("/user/history", methods=["GET"])
@token_required
def get_user_history(current_user_id):
    history = DesignHistory.query.filter_by(user_id=current_user_id).order_by(DesignHistory.created_at.desc()).all()
    output = []
    for item in history:
        output.append({
            "id": item.id,
            "theme": item.theme,
            "space_type": item.space_type,
            "budget": item.budget,
            "total_cost": item.total_cost,
            "selected_plan": item.selected_plan,
            "image_url": item.image_url,
            "created_at": item.created_at.strftime("%Y-%m-%d %H:%M")
        })
    return jsonify(output)

@app.route("/admin/stats", methods=["GET"])
@token_required
def get_admin_stats(current_user_id):
    admin = User.query.get(current_user_id)
    if not admin or not admin.is_admin:
        return jsonify({"message": "Forbidden"}), 403
    
    total_users = User.query.count()
    total_designs = DesignHistory.query.count()
    
    # Simple aggregations
    avg_budget = db.session.query(db.func.avg(DesignHistory.budget)).scalar() or 0
    
    from sqlalchemy import func
    most_common_theme = db.session.query(DesignHistory.theme, func.count(DesignHistory.theme).label('count')).group_by(DesignHistory.theme).order_by(func.count(DesignHistory.theme).desc()).first()
    
    return jsonify({
        "total_users": total_users,
        "total_designs": total_designs,
        "avg_budget": round(avg_budget, 2),
        "most_common_theme": most_common_theme[0] if most_common_theme else "N/A"
    })

@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user_id):
    user = User.query.get(current_user_id)
    return jsonify({
        'message': f'Hello, {user.username}! This is a protected route.',
        'user_id': current_user_id
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)
