import os
import sys
import json
from agents.agent3 import VisualizationAgent

# Mock data
agent1_out = {
    "space_type": "living_room",
    "detected_elements": ["sofaset", "table"],
    "budget": 50000,
    "image_analysis": {
        "description": "A modern living room with a gray sofa."
    }
}

agent2_out = {
    "theme": "contemporary_indian",
    "required_items": [
        {"item_type": "cushion", "priority": 1}
    ],
    "visualization": {
        "visual_prompt": "Warm lighting with orange and gold cushions on the sofa."
    }
}

try:
    agent = VisualizationAgent()
    print("Running Agent 3...")
    result = agent.run(agent1_out, agent2_out)
    print("Result URLs:", result["image_links"])
    
    # Check if images folder has content
    img_dir = os.path.join(os.getcwd(), "images")
    files = os.listdir(img_dir)
    print("Files in images/:", files)

except Exception as e:
    print(f"Test failed: {e}")
