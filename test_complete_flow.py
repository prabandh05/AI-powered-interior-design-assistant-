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

# Mock user input
mock_input = {
    "description": "A study room with a single white desk and a black chair. The room is messy and needs more storage for books.",
    "theme": "rajasthani_mughal",
    "budget": 50000,
    "image_path": None # For now, no image to test the text-only flow
}

# Run the pipeline
pipeline = InteriorDesignPipeline(dataset)
print("--- Starting Complete Pipeline Execution ---")

try:
    result = pipeline.run(mock_input)
    print("\n[SUCCESS] PIPELINE RUN SUCCESSFUL")
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"\n[ERROR] PIPELINE FAILED with error: {e}")
    import traceback
    traceback.print_exc()
