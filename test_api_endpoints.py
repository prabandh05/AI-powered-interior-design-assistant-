import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_agent1():
    print("\n--- Testing Agent 1 ---")
    payload = {
        "description_text": "I want a royal study room with traditional Indian patterns.",
        "budget": 50000
    }
    response = requests.post(f"{BASE_URL}/agent1", json=payload)
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_agent2(agent1_output):
    print("\n--- Testing Agent 2 ---")
    response = requests.post(f"{BASE_URL}/agent2", json=agent1_output)
    print(f"Status Code: {response.status_code}")
    # print(json.dumps(response.json(), indent=2))
    print("Agent 2 returned successfully.")
    return response.json()

def test_agent3(agent1_output, agent2_output):
    print("\n--- Testing Agent 3 ---")
    payload = {
        "agent1_output": agent1_output,
        "agent2_output": agent2_output
    }
    response = requests.post(f"{BASE_URL}/agent3", json=payload)
    print(f"Status Code: {response.status_code}")
    # print(json.dumps(response.json(), indent=2))
    print("Agent 3 returned successfully.")
    return response.json()

def test_agent4():
    print("\n--- Testing Agent 4 ---")
    payload = {
        "theme": "rajasthani_mughal",
        "space_type": "study_room",
        "required_items": [
            {"item_type": "study_table", "priority": 1},
            {"item_type": "ergonomic_chair", "priority": 2}
        ],
        "budget": 50000
    }
    response = requests.post(f"{BASE_URL}/agent4", json=payload)
    print(f"Status Code: {response.status_code}")
    print("Agent 4 returned successfully.")

if __name__ == "__main__":
    try:
        a1_out = test_agent1()
        a2_out = test_agent2(a1_out)
        a3_out = test_agent3(a1_out, a2_out)
        test_agent4()
        
        print("\n--- Testing Full Pipeline (/generate-design) ---")
        full_payload = {
            "description_text": "A rustic Indian living room with low seating.",
            "budget": 60000
        }
        res = requests.post(f"{BASE_URL}/generate-design", json=full_payload)
        print(f"Full Pipeline Status: {res.status_code}")
        print("Full pipeline executed successfully.")
        
    except Exception as e:
        print(f"Error: {e}")
