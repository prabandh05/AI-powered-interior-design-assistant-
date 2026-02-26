import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Warning: Neither GEMINI_API_KEY nor GOOGLE_API_KEY found in environment variables.")

genai.configure(api_key=api_key)

from PIL import Image

def generate_response(prompt: str, model_name: str = "gemini-2.5-flash", image_path: str = None) -> str:
    """
    Helper function to generate a response from the Gemini model.
    """
    # Prepare content
    content = [prompt]
    if image_path and os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            content.append(img)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(content)
        
        if not response or not response.text:
            raise ValueError("Empty response or blocked content from Gemini.")
            
        return response.text
        
    except Exception as e:
        print(f"[GEMINI] Critical Error: {e}")
        return ""