import json
import os
import sys

# Add the project root to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from services.pipeline import InteriorDesignPipeline

# Load dataset
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "indian_interior_v2.json")
with open(DATASET_PATH) as f:
    dataset = json.load(f)

pipeline = InteriorDesignPipeline(dataset)

# --------------------------------------------------
# STEP 1: INITIAL RUN
# --------------------------------------------------
print("\n--- STEP 1: INITIAL RUN ---")
initial_input = {
    "description": "A small empty room with white walls.",
    "theme": "contemporary_indian",
    "budget": 20000
}

initial_result = pipeline.run(initial_input)
print(f"Status: {initial_result['status']}")
print(f"Initial Theme: {initial_result['scene_analysis']['theme']}")
print(f"Initial Budget: {initial_result['scene_analysis']['budget']}")

# --------------------------------------------------
# STEP 2: ITERATION RUN (Change Theme and Budget)
# --------------------------------------------------
print("\n--- STEP 2: ITERATION RUN (Theme: Rajasthani, Budget: 80000) ---")
iteration_input = {
    "previous_scene_data": initial_result["scene_analysis"], # Passing back the scene data
    "theme": "rajasthani_mughal",
    "budget": 80000
}

iteration_result = pipeline.run(iteration_input)
print(f"Status: {iteration_result['status']}")
print(f"Is Iteration: {iteration_result['is_iteration']}")
print(f"New Theme: {iteration_result['scene_analysis']['theme']}")
print(f"New Budget: {iteration_result['scene_analysis']['budget']}")
print(f"Design Summary Content: {iteration_result['design_strategy']['summary'][:50]}...")
