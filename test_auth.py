import requests
import time
import uuid

# Base URL of the running Flask application
BASE_URL = 'http://127.0.0.1:8000'

def run_auth_tests():
    # 1. Generate a unique username for testing
    unique_id = str(uuid.uuid4())[:8]
    username = f"user_{unique_id}"
    password = "securepassword123"
    
    print(f"--- Starting Auth Tests for user: {username} ---")

    # 2. Test Registration
    print("\n[1/4] Testing Registration...")
    reg_payload = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/register", json=reg_payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code != 201:
        print("Registration failed. Stopping tests.")
        return

    # 3. Test Login
    print("\n[2/4] Testing Login...")
    login_payload = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/login", json=login_payload)
    print(f"Status: {response.status_code}")
    res_data = response.json()
    print(f"Response: {res_data}")
    
    token = res_data.get('token')
    if not token:
        print("Login failed (no token). Stopping tests.")
        return

    # 4. Test Protected Route (with JWT)
    print("\n[3/4] Testing Protected Route (Accessing with Token)...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{BASE_URL}/protected", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # 5. Test Logout
    print("\n[4/4] Testing Logout (Stateless JWT verification)...")
    # Note: In this JWT implementation, logout is handled by the client discarding the token.
    # The endpoint simply verifies that the token provided is still valid.
    response = requests.post(f"{BASE_URL}/logout", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    print("\n--- Auth Tests Completed ---")

if __name__ == "__main__":
    try:
        run_auth_tests()
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to the server at {BASE_URL}. Make sure 'python3 app.py' is running.")
