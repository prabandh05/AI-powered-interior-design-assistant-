import os
import json
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from models import db, User
from auth_utils import encode_token, token_required
from dotenv import load_dotenv
from services.pipeline import InteriorDesignPipeline

load_dotenv()

app = Flask(__name__)

# Configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'users.db')
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "indian_interior_v2.json")

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

# --- Authentication Routes ---

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'message': 'User already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
    new_user = User(username=data.get('username'), password_hash=hashed_password)
    
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
            'token': token
        }), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user_id):
    return jsonify({'message': 'Successfully logged out'}), 200

# --- Core AI Interior Routes ---

@app.route("/generate-design", methods=["POST"])
# @token_required # Uncomment if you want to protect this route
def generate_design():
    user_input = request.json
    if not user_input:
        return jsonify({"status": "error", "message": "No input provided"}), 400
    result = pipeline.run(user_input)
    return jsonify(result)

@app.route("/agent1", methods=["POST"])
def test_agent1():
    data = request.json
    result = pipeline.agent1.run(data)
    return jsonify(result)

@app.route("/agent2", methods=["POST"])
def test_agent2():
    data = request.json
    result = pipeline.agent2.run(data)
    return jsonify(result)

@app.route("/agent3", methods=["POST"])
def test_agent3():
    data = request.json
    agent1_output = data.get("agent1_output")
    agent2_output = data.get("agent2_output")
    result = pipeline.agent3.run(agent1_output, agent2_output)
    return jsonify(result)

@app.route("/agent4", methods=["POST"])
def test_agent4():
    data = request.json
    result = pipeline.agent4.generate_comparison_plans(
        theme=data["theme"],
        space_type=data["space_type"],
        required_items=data["required_items"],
        user_budget=data["budget"]
    )
    return jsonify(result)

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
