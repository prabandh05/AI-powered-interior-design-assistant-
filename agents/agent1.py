import json
import re
import sys
import os
from typing import Dict, Any

# Add the project root to sys.path to allow importing from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gemini_client import generate_response


class SceneStructuringAgent:
    """
    Agent 1: Scene Structuring Agent

    Converts raw user input into a normalized structured JSON format
    that downstream agents can safely consume.
    """

    DEFAULT_BUDGET = 20000
    ALLOWED_THEMES = ["traditional_indian", "contemporary_indian", "rustic_indian", "rajasthani_mughal"]

    def __init__(self):
        pass

    def run(self, user_input: Dict[str, Any], image_path: str = None) -> Dict[str, Any]:
        """
        Main execution method.

        :param user_input: Raw form data
        :param image_path: Optional path to an uploaded image
        :return: Structured scene JSON
        """

        prompt = self._build_prompt(user_input, has_image=bool(image_path))

        response_text = generate_response(prompt, image_path=image_path)

        structured_output = self._safe_json_parse(response_text)

        if structured_output is None:
            print("Warning: Falling back to deterministic response.")
            structured_output = self._fallback_response(user_input)

        validated_output = self._validate_output(structured_output)

        return validated_output

    # -----------------------------
    # Prompt Builder
    # -----------------------------

    def _build_prompt(self, user_input: Dict[str, Any], has_image: bool = False) -> str:
        image_instruction = ""
        if has_image:
            image_instruction = """
- Analyze the provided IMAGE carefully.
- Identify the room's current layout and existing furniture.
- Suggest if the image is a 'current_state' or a 'reference_preference'.
- Extract dominant colors and materials from the image.
"""

        return f"""
You are a Professional Interior Scene Structuring Agent.

Your job is to convert raw user input (text and optional image) into STRICT structured JSON.

Analyze:
- description_text
- preferred_theme
- budget
{image_instruction}

Infer:
- space_type (living_room, bedroom, kitchen, study_room)
- detected_elements (list of furniture or features mentioned in text OR seen in image)
- theme (must be one of: traditional_indian, contemporary_indian, rustic_indian, rajasthani_mughal)
- budget (integer)
- image_analysis (object containing: description, detected_elements, dominant_colors, style_type)

RULES:
- Respond ONLY in valid JSON.
- Do NOT include markdown blocks.
- If theme is missing, default to traditional_indian.
- If budget is missing, default to 20000.
- If you include anything outside the JSON object, the system will reject your output.

Required Output Format:
{{
  "space_type": "",
  "detected_elements": [],
  "theme": "",
  "budget": 0,
  "image_analysis": {{
    "description": "",
    "detected_elements": [],
    "dominant_colors": [],
    "style_type": "current_state | reference_preference | none"
  }}
}}

User Input:
{json.dumps(user_input, indent=2)}
"""

    # -----------------------------
    # Safe JSON Parsing
    # -----------------------------

    def _safe_json_parse(self, response_text: str):

        try:
            cleaned = response_text.strip()

            # Remove markdown blocks if Gemini adds them
            if cleaned.startswith("```"):
                cleaned = re.sub(r"```(?:json)?", "", cleaned)
                cleaned = cleaned.replace("```", "").strip()

            return json.loads(cleaned)

        except Exception as e:
            print("JSON parsing failed:", e)
            print("Raw response:", response_text)
            return None

    # -----------------------------
    # Output Validation Layer
    # -----------------------------

    def _validate_output(self, data: Dict[str, Any]) -> Dict[str, Any]:

        if not isinstance(data, dict):
            return self._fallback_response({})

        # Space Type Validation
        space_type = data.get("space_type", "living_room")
        if not space_type:
            space_type = "living_room"

        # Detected Elements Validation
        detected_elements = data.get("detected_elements", [])
        if not isinstance(detected_elements, list):
            detected_elements = []

        # Theme Validation
        theme_raw = str(data.get("theme", "")).lower().strip()
        theme_mapping = {
            "traditional indian": "traditional_indian",
            "traditional_indian": "traditional_indian",
            "contemporary indian": "contemporary_indian",
            "contemporary_indian": "contemporary_indian",
            "rustic indian": "rustic_indian",
            "rustic_indian": "rustic_indian",
            "rajasthani – mughal style": "rajasthani_mughal",
            "rajasthani mughal style": "rajasthani_mughal",
            "rajasthani_mughal": "rajasthani_mughal"
        }
        theme = theme_mapping.get(theme_raw, "traditional_indian")

        # Budget Validation
        try:
            budget = int(data.get("budget", self.DEFAULT_BUDGET))
        except:
            budget = self.DEFAULT_BUDGET

        if budget <= 0:
            budget = self.DEFAULT_BUDGET

        # Image Analysis Validation
        image_analysis = data.get("image_analysis", {})
        if not isinstance(image_analysis, dict):
            image_analysis = {}
        
        image_detected = image_analysis.get("detected_elements", [])
        if not isinstance(image_detected, list):
            image_detected = []
            
        dominant_colors = image_analysis.get("dominant_colors", [])
        if not isinstance(dominant_colors, list):
            dominant_colors = []
        
        return {
            "space_type": space_type,
            "detected_elements": detected_elements,
            "theme": theme,
            "budget": budget,
            "image_analysis": {
                "description": image_analysis.get("description", ""),
                "detected_elements": image_detected,
                "dominant_colors": dominant_colors,
                "style_type": image_analysis.get("style_type", "none")
            }
        }

    # -----------------------------
    # Fallback Mechanism
    # -----------------------------

    def _fallback_response(self, user_input: Dict[str, Any]) -> Dict[str, Any]:

        try:
            budget = int(user_input.get("budget", self.DEFAULT_BUDGET))
        except:
            budget = self.DEFAULT_BUDGET

        theme = user_input.get("preferred_theme", "traditional_indian")
        if theme not in self.ALLOWED_THEMES:
            theme = "traditional_indian"

        return {
            "space_type": "living_room",
            "detected_elements": [],
            "theme": theme,
            "budget": budget,
            "image_analysis": {
                "description": "No image provided or analysis failed.",
                "detected_elements": [],
                "dominant_colors": [],
                "style_type": "none"
            }
        }


# -----------------------------
# Test the Agent
# -----------------------------
if __name__ == "__main__":
    test_input = {
        "description_text": "This is my home office/study area. I have a desk and a whiteboard here. I want to transform this into a space with a Rajasthani – Mughal theme while keeping it functional for work.",
        "preferred_theme": "rajasthani_mughal",
        "budget": "60000"
    }

    # Path to test image
    image_path = r"C:\Users\praba\OneDrive\Desktop\Hackathon\Gruha Assistant\images\current\WhatsApp Image 2026-02-26 at 12.55.37 PM.jpeg"

    agent = SceneStructuringAgent()
    result = agent.run(test_input, image_path=image_path)

    print("\n--- Agent 1 Output ---")
    print(json.dumps(result, indent=2))
