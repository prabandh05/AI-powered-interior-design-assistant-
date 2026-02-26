from utils.gemini_client import generate_response

test_prompt = "Say hello"
try:
    response = generate_response(test_prompt, model_name="gemini-2.5-flash")
    if response:
        print(f"Gemini 1.5 success: {response}")
    else:
        print("Gemini 1.5 failed: Empty response")
except Exception as e:
    print(f"Gemini 1.5 error: {e}")
