import requests
import json

url = "http://127.0.0.1:5000/generate-design"
payload = {
    "description": "Small home office with a white desk and rolling chair.",
    "theme": "rajasthani_mughal",
    "budget": 30000
}
headers = {'Content-Type': 'application/json'}

try:
    print(f"Sending request to {url}...")
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"Status Code: {response.status_code}")
    print("\n[RESPONSE DATA]")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Request failed: {e}")
