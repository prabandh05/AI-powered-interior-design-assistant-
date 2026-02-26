import os
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from models import db, User
from auth_utils import encode_token, token_required
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'users.db')
if not os.path.exists(os.path.dirname(DB_PATH)):
    os.makedirs(os.path.dirname(DB_PATH))

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key-for-dev')

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return jsonify({"message": "Welcome to AI Interior Design Assistant API"})

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
