import json
import os
from app import app, db
from models import User

def test():
    with app.app_context():
        # Mock user input
        user_input = {
            "description_text": "I want a royal study room",
            "theme": "rajasthani_mughal",
            "budget": 50000
        }
        
        # We can call the pipeline directly through the app's pipeline instance if accessible,
        # but let's just import it.
        from services.pipeline import InteriorDesignPipeline
        from app import dataset
        
        pipeline = InteriorDesignPipeline(dataset)
        result = pipeline.run(user_input)
        
        print("\n=== PIPELINE RESULT ===")
        print(f"Status: {result.get('status')}")
        print(f"Procurement Plans found: {len(result.get('procurement', {}).get('comparison_plans', []))}")
        
        if result.get('procurement', {}).get('comparison_plans'):
            for plan in result['procurement']['comparison_plans']:
                print(f"Plan: {plan.get('plan_name')}, Items: {len(plan.get('items', []))}")
        else:
            print("WARNING: NO PLANS FOUND")

if __name__ == "__main__":
    test()
