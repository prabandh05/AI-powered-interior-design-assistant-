import jwt
import datetime
from flask import request, jsonify
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env

SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-for-dev')

def encode_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
            'iat': datetime.datetime.now(datetime.timezone.utc),
            'sub': str(user_id)
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return str(e)

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return int(payload['sub'])
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        user_id_or_msg = decode_token(token)
        if isinstance(user_id_or_msg, str):
             return jsonify({'message': user_id_or_msg}), 401
        
        return f(user_id_or_msg, *args, **kwargs)
    
    return decorated
