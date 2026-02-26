import requests
import json
import os

BASE_URL = "http://127.0.0.1:5000"

def stress_test_1_empty_items():
    print("\n[TEST 1] Empty Required Items Case")
    payload = {
        "theme": "rajasthani_mughal",
        "space_type": "study_room",
        "required_items": [],
        "budget": 50000
    }
    response = requests.post(f"{BASE_URL}/agent4", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json()[0], indent=2))

def stress_test_2_low_budget():
    print("\n[TEST 2] Budget = Very Low (2000)")
    payload = {
        "theme": "rajasthani_mughal",
        "space_type": "study_room",
        "required_items": [{"item_type": "study_table", "priority": 1}],
        "budget": 2000
    }
    response = requests.post(f"{BASE_URL}/agent4", json=payload)
    print(f"Status: {response.status_code}")
    # Low budget plan (usually Plan 3)
    print(json.dumps(response.json(), indent=2))

def stress_test_3_theme_not_in_dataset():
    print("\n[TEST 3] Theme Not In Dataset (modern_scandinavian)")
    payload = {
        "theme": "modern_scandinavian",
        "space_type": "study_room",
        "required_items": [{"item_type": "study_table", "priority": 1}],
        "budget": 50000
    }
    response = requests.post(f"{BASE_URL}/agent4", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json()[0], indent=2))

if __name__ == "__main__":
    stress_test_1_empty_items()
    stress_test_2_low_budget()
    stress_test_3_theme_not_in_dataset()
