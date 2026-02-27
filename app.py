import os
import json
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client

# Relative imports from the project
from auth_utils import token_required, decode_token
from services.pipeline import InteriorDesignPipeline

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

app.config['JSON_SORT_KEYS'] = False

# Supabase Configurations
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Local Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "indian_interior_v2.json")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
IMAGES_FOLDER = os.path.join(BASE_DIR, "images")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Enumerated Locations
SUPPORTED_LOCATIONS = [
    "Mumbai, MH", "Delhi, DL", "Bangalore, KA", "Hyderabad, TG",
    "Chennai, TN", "Kolkata, WB", "Pune, MH", "Jaipur, RJ"
]

# Load dataset and initialize pipeline
with open(DATASET_PATH) as f:
    dataset = json.load(f)
pipeline = InteriorDesignPipeline(dataset)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to AI Interior Design Assistant API (Supabase Cloud Mode)"})

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_FOLDER, filename)

@app.route('/api/locations', methods=['GET'])
def get_locations():
    return jsonify(SUPPORTED_LOCATIONS)

# --- Authentication Routes ---

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password') or not data.get('email') or not data.get('name'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    # 1. Sign up user in Supabase Auth
    try:
        auth_res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "name": data.get('name'),
                    "username": data.get('username')
                }
            }
        })
        
        if not auth_res.user:
            return jsonify({'message': 'Registration failed'}), 400
            
        user_id = auth_res.user.id
        
        # 2. Insert extra profile data into our profiles table
        location = data.get('location', SUPPORTED_LOCATIONS[0])
        if location not in SUPPORTED_LOCATIONS:
            location = SUPPORTED_LOCATIONS[0]

        profile_data = {
            "id": user_id,
            "name": data.get('name'),
            "username": data.get('username'),
            "email": email,
            "location": location,
            "is_admin": data.get('is_admin', False)
        }
        
        supabase.table("profiles").insert(profile_data).execute()
        
        return jsonify({'message': 'User registered successfully. Please check your email for verification if enabled.'}), 201
        
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing fields'}), 400
    
    # In Supabase, we usually login with email. If the user provides a username, 
    # we first need to find the email associated with that username.
    username_or_email = data.get('username')
    password = data.get('password')
    
    email = username_or_email
    name = ""
    is_admin = False
    
    if "@" not in username_or_email:
        # It's a username, find email in profiles
        try:
            profile_res = supabase.table("profiles").select("email, name, is_admin").eq("username", username_or_email).execute()
            if not profile_res.data:
                return jsonify({'message': 'User not found'}), 404
            email = profile_res.data[0]['email']
            name = profile_res.data[0]['name']
            is_admin = profile_res.data[0]['is_admin']
        except Exception as e:
            return jsonify({'message': str(e)}), 400
    else:
        # Attempt to get name/is_admin for response
        try:
            profile_res = supabase.table("profiles").select("name, is_admin").eq("email", email).execute()
            if profile_res.data:
                name = profile_res.data[0]['name']
                is_admin = profile_res.data[0]['is_admin']
        except:
            pass

    try:
        auth_res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if not auth_res.session:
            return jsonify({'message': 'Invalid credentials'}), 401
            
        return jsonify({
            'message': 'Login successful',
            'token': auth_res.session.access_token,
            'is_admin': is_admin,
            'name': name
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 401

@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user_id):
    try:
        supabase.auth.sign_out()
        return jsonify({'message': 'Successfully logged out'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# --- Core AI Interior Routes ---

@app.route("/generate-design", methods=["POST"])
def generate_design():
    auth_header = request.headers.get('Authorization')
    current_user_id = None
    if auth_header:
        try:
            token = auth_header.split(" ")[1]
            current_user_id = decode_token(token)
        except:
            pass

    if request.is_json:
        user_input = request.json
    else:
        user_input = {
            "description_text": request.form.get("description_text"),
            "theme": request.form.get("theme"),
            "budget": request.form.get("budget"),
        }
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

    if current_user_id and result.get("status") == "success":
        try:
            history_data = {
                "user_id": current_user_id,
                "theme": result["design_strategy"].get("theme", ""),
                "space_type": result["design_strategy"].get("space_type", ""),
                "budget": int(user_input.get("budget", 0)),
                "total_cost": result["procurement"]["comparison_plans"][0].get("total_cost", 0) if result["procurement"]["comparison_plans"] else 0,
                "selected_plan": result["procurement"]["comparison_plans"][0].get("plan_name", "") if result["procurement"]["comparison_plans"] else "Generic",
                "design_intensity": result["visuals"].get("used_intensity", "moderate"),
                "image_url": result["visuals"]["image_links"][0] if result["visuals"]["image_links"] else "",
                "procurement_plans_json": json.dumps(result["procurement"].get("comparison_plans", []))
            }
            supabase.table("design_history").insert(history_data).execute()
        except Exception as e:
            print(f"Error saving history: {e}")

    return jsonify(result)

@app.route("/user/history", methods=["GET"])
@token_required
def get_user_history(current_user_id):
    try:
        res = supabase.table("design_history").select("*").eq("user_id", current_user_id).order("created_at", desc=True).execute()
        output = []
        for item in res.data:
            output.append({
                "id": item['id'],
                "theme": item['theme'],
                "space_type": item['space_type'],
                "budget": item['budget'],
                "total_cost": item['total_cost'],
                "selected_plan": item['selected_plan'],
                "image_url": item['image_url'],
                "procurement_plans": json.loads(item['procurement_plans_json']) if item['procurement_plans_json'] else [],
                "created_at": item['created_at']
            })
        return jsonify(output)
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route("/admin/stats", methods=["GET"])
@token_required
def get_admin_stats(current_user_id):
    # Verify admin status from profiles
    try:
        profile_res = supabase.table("profiles").select("is_admin").eq("id", current_user_id).execute()
        if not profile_res.data or not profile_res.data[0]['is_admin']:
             return jsonify({"message": "Forbidden"}), 403
    except:
        return jsonify({"message": "Forbidden"}), 403
    
    try:
        # Get total users and designs
        total_users = supabase.table("profiles").select("id", count="exact").execute().count
        total_designs_res = supabase.table("design_history").select("id", count="exact").execute()
        total_designs = total_designs_res.count
        
        # Get all design records for processing (Supabase doesn't support complex aggregations like case in simple client)
        designs = supabase.table("design_history").select("*").execute().data
        
        if not designs:
             return jsonify({
                "total_users": total_users,
                "total_designs": 0,
                "avg_budget": 0,
                "theme_distribution": [],
                "budget_distribution": [],
                "location_distribution": [],
                "heatmap_data": [],
                "trend": []
            })

        # Process stats in Python
        budgets = [d['budget'] for d in designs]
        avg_budget = sum(budgets) / len(budgets) if budgets else 0
        
        from collections import Counter
        
        # 1. Theme distribution
        themes = [d['theme'].replace('_', ' ').title() for d in designs]
        theme_counts = Counter(themes)
        theme_distribution = [{"name": k, "value": v} for k,v in theme_counts.items()]
        
        # 2. Budget distribution
        tiers = []
        for b in budgets:
            if b < 30000: tiers.append("Economy")
            elif b < 70000: tiers.append("Mid-Range")
            elif b < 120000: tiers.append("Premium")
            else: tiers.append("Luxury")
        tier_counts = Counter(tiers)
        budget_distribution = [{"name": k, "value": v} for k,v in tier_counts.items()]
        
        # 3. Location distribution
        # Need to join profiles. We'll fetch all profiles and join in memory for simplicity
        profiles = {p['id']: p['location'] for p in supabase.table("profiles").select("id, location").execute().data}
        locations = [profiles.get(d['user_id'], "Other").split(',')[0] for d in designs]
        loc_counts = Counter(locations)
        location_distribution = [{"name": k, "value": v} for k, v in loc_counts.items()]
        
        # 4. Heatmap Data (Theme vs Space Type)
        matrix = {}
        for d in designs:
            th = d['theme'].replace('_', ' ').title()
            sp = d['space_type'].replace('_', ' ').title()
            if th not in matrix: matrix[th] = {"name": th}
            matrix[th][sp] = matrix[th].get(sp, 0) + 1
        heatmap_data = list(matrix.values())
        
        # 5. Trend
        from datetime import datetime
        dates = [d['created_at'][:10] for d in designs]
        date_counts = Counter(dates)
        trend = [{"date": k, "count": v} for k,v in sorted(date_counts.items())]

        return jsonify({
            "total_users": total_users,
            "total_designs": total_designs,
            "avg_budget": round(avg_budget, 2),
            "theme_distribution": theme_distribution,
            "budget_distribution": budget_distribution,
            "location_distribution": location_distribution,
            "heatmap_data": heatmap_data,
            "trend": trend
        })
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user_id):
    try:
        res = supabase.table("profiles").select("*").eq("id", current_user_id).execute()
        user = res.data[0]
        return jsonify({
            'message': f'Hello, {user["name"]}! This is a protected route.',
            'user_id': current_user_id
        }), 200
    except:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=8000)
