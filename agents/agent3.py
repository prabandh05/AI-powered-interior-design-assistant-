import os
import sys
import json
from typing import Dict, Any, List
from bytez import Bytez
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()


class VisualizationAgent:

    def __init__(self):
        api_key = os.getenv("BYTEZ_API_KEY")
        if not api_key:
            raise ValueError("BYTEZ_API_KEY not found in environment variables")

        self.sdk = Bytez(api_key)
        self.model = self.sdk.model("google/imagen-4.0-ultra-generate-001")

    # --------------------------------------------------
    # Budget Tier Logic
    # --------------------------------------------------

    def _get_design_intensity(self, budget: int) -> str:
        try:
            budget = int(budget)
        except:
            budget = 30000

        if budget < 25000:
            return "minimal"
        elif budget < 60000:
            return "moderate"
        else:
            return "luxury"

    # --------------------------------------------------
    # CLEAN Image Prompt Builder (Concise + Controlled)
    # --------------------------------------------------

    def _build_prompt(self, agent1_output: Dict[str, Any], agent2_output: Dict[str, Any]) -> str:

        image_analysis = agent1_output.get("image_analysis", {})
        visualization = agent2_output.get("visualization", {})

        base_description = image_analysis.get("description", "")
        detected_elements = agent1_output.get("detected_elements", [])
        theme = agent2_output.get("theme", "").replace("_", " ")
        visual_prompt = visualization.get("visual_prompt", "")
        budget = agent1_output.get("budget", 30000)

        intensity = self._get_design_intensity(budget)

        # 🔥 Strict richness control
        if intensity == "minimal":
            intensity_block = """
Minimal redesign.
Simple thematic touches.
Limited decorative elements.
Affordable materials.
Clean walls and subtle lighting.
"""
        elif intensity == "moderate":
            intensity_block = """
Balanced redesign.
Noticeable decor.
Layered textiles.
Elegant but not overly opulent.
"""
        else:
            intensity_block = """
Luxurious redesign.
Rich textiles.
Ornate carved elements.
Layered patterns.
Premium materials like brass, silk, carved wood.
"""

        # Clean, structured, image-model-friendly prompt
        final_prompt = f"""
Interior redesign of a {theme} style {agent1_output.get("space_type", "room")}.

Original Room:
{base_description}

Keep existing elements:
{", ".join(detected_elements)}

Apply this concept:
{visual_prompt}

Design Intensity:
{intensity_block}

Maintain realistic proportions and layout.
Photorealistic interior design photography.
High resolution.
Natural lighting.
Realistic materials and textures.
"""

        return final_prompt.strip()

    # --------------------------------------------------
    # Image Generation
    # --------------------------------------------------

    def generate_image(self, agent1_output: Dict[str, Any], agent2_output: Dict[str, Any]) -> Dict[str, Any]:

        prompt = self._build_prompt(agent1_output, agent2_output)
        intensity = self._get_design_intensity(agent1_output.get("budget"))

        print(f"\n--- Generating Image | Budget Tier: {intensity.upper()} ---")
        
        try:
            results = self.model.run(prompt)
            
            if results.error:
                return {
                    "error": str(results.error),
                    "image": None,
                    "used_intensity": intensity
                }
            
            return {
                "error": None,
                "image": results.output,
                "used_intensity": intensity
            }
        except Exception as e:
            print(f"Agent 3 Image Generation Error: {e}")
            return {
                "error": str(e),
                "image": None,
                "used_intensity": intensity
            }

    # --------------------------------------------------
    # LLM Guide (Separate from Image Logic)
    # --------------------------------------------------

    def generate_guide(self, agent1_output: Dict[str, Any], agent2_output: Dict[str, Any]) -> str:
        from utils.gemini_client import generate_response

        theme = agent2_output.get("theme", "traditional_indian").replace("_", " ")
        budget = agent1_output.get("budget", 30000)
        items = agent2_output.get("required_items", [])
        space = agent1_output.get("space_type", "room")

        prompt = f"""
You are a Professional Interior Architect.

Create 3 distinct design concepts for a {theme} themed {space}.
Budget: {budget} INR.

Recommended Items:
{json.dumps(items, indent=2)}

For EACH concept:
- Provide a strong title
- Write a descriptive paragraph
- Provide 3–4 clear execution steps

Keep it exciting but practical.
Avoid excessive fluff.
No markdown.
"""

        return generate_response(prompt)

    # --------------------------------------------------
    # Main Runner
    # --------------------------------------------------

    def run(self, agent1_output: Dict[str, Any], agent2_output: Dict[str, Any]) -> Dict[str, Any]:

        visual_res = self.generate_image(agent1_output, agent2_output)
        text_guide = self.generate_guide(agent1_output, agent2_output)

        links: List[str] = []
        if visual_res["image"]:
            raw_data = visual_res["image"]
            if not isinstance(raw_data, list):
                raw_data = [raw_data]

            for item in raw_data:
                if isinstance(item, str) and item.startswith("http"):
                    links.append(item)

        return {
            "visuals": visual_res,
            "image_links": links,
            "guide": text_guide
        }


# --------------------------------------------------
# Standalone Test
# --------------------------------------------------

if __name__ == "__main__":

    agent1_out = {
        "space_type": "study_room",
        "detected_elements": ["desk", "monitor", "whiteboard"],
        "budget": 15000,
        "image_analysis": {
            "description": "A functional home office with a white desk and standard peripherals."
        }
    }

    agent2_out = {
        "theme": "rajasthani_mughal",
        "required_items": [
            {"item_type": "wall_art", "priority": 1},
            {"item_type": "accent_wall_paint", "priority": 2}
        ],
        "visualization": {
            "visual_prompt": "Terracotta accent wall with a single framed Rajasthani art piece and warm desk lighting."
        }
    }

    agent = VisualizationAgent()
    result = agent.run(agent1_out, agent2_out)

    print("\n==============================")
    print("      GENERATED IMAGE LINKS")
    print("==============================\n")
    if result["image_links"]:
        for link in result["image_links"]:
            print(f"URL: {link}")
    else:
        print("No image links found.")

    print("\n==============================")
    print("     TEXTUAL DESIGN GUIDE")
    print("==============================\n")
    if result["guide"] and len(result["guide"]) > 10:
        print(result["guide"])
    else:
        print("Error: Design guide text was empty or too short. Check your Gemini API key and prompt.")
    
    print("\n==============================\n")
