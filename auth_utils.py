import os
from functools import wraps
from flask import request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
        
        try:
            # Verify the token with Supabase and get user
            res = supabase.auth.get_user(token)
            if not res.user:
                return jsonify({'message': 'Invalid token. Please log in again.'}), 401
            
            # Extract user_id from the response
            current_user_id = res.user.id
            
        except Exception as e:
            return jsonify({'message': f'Invalid token: {str(e)}'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

# These are no longer needed for Supabase as it handles encoding/decoding
def encode_token(user_id):
    pass

def decode_token(token):
    try:
        res = supabase.auth.get_user(token)
        if res.user:
            return res.user.id
        return 'Invalid token.'
    except:
        return 'Invalid token.'
