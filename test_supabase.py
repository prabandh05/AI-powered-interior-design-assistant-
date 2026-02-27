import requests
import uuid
import time

BASE_URL = 'http://127.0.0.1:8000'

def test_supabase_auth():
    print("--- Supabase Migration Verification ---")
    
    unique_id = str(uuid.uuid4())[:8]
    username = f"supa_{unique_id}"
    email = f"{username}@testmail.com"
    password = "TestPassword123!"
    
    # 1. Register
    print(f"\n[1/3] Registering user: {username}")
    reg_data = {
        "name": "Supabase Tester",
        "username": username,
        "email": email,
        "password": password
    }
    try:
        r = requests.post(f"{BASE_URL}/register", json=reg_data)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.json()}")
    except Exception as e:
        print(f"Request failed: {e}")
        return

    # 2. Login
    print("\n[2/3] Logging in...")
    login_data = {
        "username": username, # Logging in with username (handles email lookup in app.py)
        "password": password
    }
    r = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Status: {r.status_code}")
    res = r.json()
    token = res.get('token')
    print(f"Token received: {'Yes' if token else 'No'}")

    # 3. Access Protected Route
    if token:
        print("\n[3/3] Accessing Protected Route...")
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(f"{BASE_URL}/protected", headers=headers)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.json()}")

if __name__ == "__main__":
    test_supabase_auth()
