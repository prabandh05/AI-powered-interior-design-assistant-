import requests

BASE_URL = 'http://127.0.0.1:8000'

def test_login_only():
    print("\n[DEBUG] Testing login for supa_b5270a1c...")
    login_data = {
        "username": "supa_b5270a1c",
        "password": "TestPassword123!"
    }
    r = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")

if __name__ == "__main__":
    test_login_only()
