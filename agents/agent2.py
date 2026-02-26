import json
import re
import sys
import os
from typing import Dict, Any, List

# Add the project root to sys.path to allow importing from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gemini_client import generate_response


class DesignPlannerAgent:
    """
    Agent 2: Interior Design Planner Agent

    Converts structured scene data into:
    - Design summary
    - Required item list (conceptual only)
    - Visualization instructions

    No prices. No product links. No brands.
    """

    ALLOWED_ITEM_TYPES = [
        "study_table",
        "ergonomic_chair",
        "bookshelf",
        "wall_art",
        "wall_panel",
        "floor_lamp",
        "ceiling_light",
        "carpet",
        "curtains",
        "storage_unit",
        "decor_statue",
        "accent_wall_paint"
    ]

    ALLOWED_CATEGORIES = [
        "furniture",
        "lighting",
        "decor",
        "textile",
        "storage",
        "wall_treatment"
    ]

    def __init__(self):
        pass

    # -----------------------------
    # Main Execution
    # -----------------------------

    def run(self, scene_data: Dict[str, Any]) -> Dict[str, Any]:

        prompt = self._build_prompt(scene_data)

        try:
            response_text = generate_response(prompt)
        except Exception as e:
            print(f"Agent 2 API Error: {e}")
            response_text = ""

        parsed_output = self._safe_json_parse(response_text)

        if parsed_output is None:
            print("Warning: Falling back to safe planner output.")
            return self._fallback_response(scene_data)

        validated_output = self._validate_output(parsed_output, scene_data)

        return validated_output

    # -----------------------------
    # Prompt Builder
    # -----------------------------

    def _build_prompt(self, scene_data: Dict[str, Any]) -> str:

        return f"""
You are a Professional Interior Design Planner Agent.

You receive structured scene data and must generate a culturally accurate, space-aware design plan.

STRICT RULES:

1. Use ONLY the following item_type values:
study_table, ergonomic_chair, bookshelf, wall_art, wall_panel,
floor_lamp, ceiling_light, carpet, curtains,
storage_unit, decor_statue, accent_wall_paint

2. Use ONLY these categories:
furniture, lighting, decor, textile, storage, wall_treatment

3. DO NOT recommend items already present in detected_elements.

4. DO NOT include product names or prices.

5. Maximum 6 required_items.

6. Priorities must be integers starting from 1.

7. Respect the theme exactly as provided.

8. Respond ONLY in valid JSON.
Do not include markdown.
Do not include explanations.

Required Output Format:

{{
  "design_summary": "",
  "space_type": "",
  "theme": "",
  "required_items": [
    {{
      "item_type": "",
      "category": "",
      "priority": 0,
      "placement": "",
      "reason": ""
    }}
  ],
  "visualization": {{
    "style_keywords": [],
    "color_palette": [],
    "material_focus": [],
    "lighting_style": "",
    "visual_prompt": ""
  }}
}}

Scene Data:
{json.dumps(scene_data, indent=2)}
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
    # Validation Layer
    # -----------------------------

    def _is_redundant(self, item_type: str, detected_elements: List[str]) -> bool:
        """
        Heuristic to check if an item type is already likely present in the room.
        """
        # Synonyms for smarter deduplication
        synonyms = {
            "study_table": ["desk", "table", "workstation", "counter"],
            "ergonomic_chair": ["chair", "seating", "stool", "sofa"],
            "ceiling_light": ["lamp", "fan", "fixture", "bulb", "chandelier"],
            "bookshelf": ["shelf", "storage", "rack", "cupboard"],
            "wall_art": ["frame", "painting", "poster", "wall hanging", "clock"],
            "wall_panel": ["wallpaper", "wainscoting"],
            "carpet": ["rug", "mat", "flooring"],
            "curtains": ["blind", "drape", "shutter"]
        }

        item_type_clean = item_type.lower()
        
        for detected in detected_elements:
            detected_lower = detected.lower()
            
            # Exact match
            if item_type_clean in detected_lower or detected_lower in item_type_clean:
                return True
            
            # Synonym match
            if item_type in synonyms:
                if any(syn in detected_lower for syn in synonyms[item_type]):
                    return True
        
        return False

    def _validate_output(self, data: Dict[str, Any], scene_data: Dict[str, Any]) -> Dict[str, Any]:

        if not isinstance(data, dict):
            return self._fallback_response(scene_data)

        space_type = data.get("space_type", scene_data.get("space_type", "living_room"))
        theme = data.get("theme", scene_data.get("theme", "traditional_indian"))

        required_items = data.get("required_items", [])
        if not isinstance(required_items, list):
            required_items = []

        validated_items = []

        detected_elements = scene_data.get("detected_elements", [])

        for item in required_items:

            if not isinstance(item, dict):
                continue

            item_type = item.get("item_type", "")
            category = item.get("category", "")
            priority = item.get("priority", 0)

            # Enforce allowed vocabulary
            if item_type not in self.ALLOWED_ITEM_TYPES:
                continue

            if category not in self.ALLOWED_CATEGORIES:
                continue

            # NEW: Smarter Redundancy Check
            if self._is_redundant(item_type, detected_elements):
                continue

            try:
                priority = int(priority)
                if priority <= 0:
                    priority = 99 # Push to end if zero or negative
            except:
                priority = 99

            validated_items.append({
                "item_type": item_type,
                "category": category,
                "priority": priority,
                "placement": item.get("placement", ""),
                "reason": item.get("reason", "")
            })

        # Sort by user/llm provided priority first
        validated_items = sorted(validated_items, key=lambda x: x["priority"])

        # NEW: Enforce strict sequential ordering (1, 2, 3...)
        for i, item in enumerate(validated_items, start=1):
            item["priority"] = i

        # Limit to 6 items max
        validated_items = validated_items[:6]

        visualization = data.get("visualization", {})
        if not isinstance(visualization, dict):
            visualization = {}

        return {
            "design_summary": data.get("design_summary", ""),
            "space_type": space_type,
            "theme": theme,
            "required_items": validated_items,
            "visualization": {
                "style_keywords": visualization.get("style_keywords", []),
                "color_palette": visualization.get("color_palette", []),
                "material_focus": visualization.get("material_focus", []),
                "lighting_style": visualization.get("lighting_style", ""),
                "visual_prompt": visualization.get("visual_prompt", "")
            }
        }

    # -----------------------------
    # Fallback Mechanism
    # -----------------------------

    def _fallback_response(self, scene_data: Dict[str, Any]) -> Dict[str, Any]:

        return {
            "design_summary": "A culturally aligned enhancement plan based on the selected theme.",
            "space_type": scene_data.get("space_type", "living_room"),
            "theme": scene_data.get("theme", "traditional_indian"),
            "required_items": [],
            "visualization": {
                "style_keywords": [],
                "color_palette": [],
                "material_focus": [],
                "lighting_style": "",
                "visual_prompt": ""
            }
        }


# -----------------------------
# Test the Agent
# -----------------------------
if __name__ == "__main__":
    # Actual output from Agent 1
    agent1_output = {
        "space_type": "study_room",
        "detected_elements": [
            "desk",
            "monitor",
            "whiteboard",
            "keyboard",
            "office chair",
            "large display screen",
            "small wooden shelf",
            "small table",
            "bulletin board",
            "wall clock"
        ],
        "theme": "rajasthani_mughal",
        "budget": 75000,
        "image_analysis": {
            "description": "The image shows a plain and functional workspace... somewhat bare.",
            "detected_elements": [
                "desk",
                "monitor",
                "keyboard",
                "office chair",
                "whiteboard",
                "large display screen",
                "small wooden shelf",
                "small table",
                "bulletin board",
                "wall clock"
            ],
            "dominant_colors": [
                "cream",
                "white",
                "black",
                "brown",
                "silver",
                "red",
                "beige"
            ],
            "style_type": "current_state"
        }
    }

    agent = DesignPlannerAgent()
    result = agent.run(agent1_output)

    print("\n--- Agent 2 Output ---")
    print(json.dumps(result, indent=2))

    # Save to file for easy reading
    with open("agent2_test_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print("\n[Result also saved to agent2_test_output.json]")
