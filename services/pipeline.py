import os
from typing import Dict, Any
from agents.agent1 import SceneStructuringAgent
from agents.agent2 import DesignPlannerAgent
from agents.agent3 import VisualizationAgent
from agents.agent4 import Agent4ProcurementEngine

class InteriorDesignPipeline:
    def __init__(self, dataset: Dict[str, Any]):
        self.agent1 = SceneStructuringAgent()
        self.agent2 = DesignPlannerAgent()
        self.agent3 = VisualizationAgent()
        self.agent4 = Agent4ProcurementEngine(dataset)

    def run(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates the four agents. Supports iterations (skipping Agent 1).
        """
        # --- PHASE 1: Scene Structuring (or Iteration) ---
        previous_scene = user_input.get("previous_scene_data")
        
        if previous_scene:
            # ITERATION MODE: Skip Agent 1, use previous data
            print("\n[PIPELINE] Detected Iteration Mode. Skipping Agent 1...")
            scene_data = previous_scene
            
            # Update specific fields if the user provided new ones
            if "theme" in user_input:
                scene_data["theme"] = user_input["theme"]
            if "budget" in user_input:
                try:
                    scene_data["budget"] = int(user_input["budget"])
                except:
                    pass
        else:
            # INITIAL MODE: Run Agent 1
            print("\n[PIPELINE] Initial Run. Calling Agent 1...")
            image_path = user_input.get("image_path")
            scene_data = self.agent1.run(user_input, image_path=image_path)

        # --- PHASE 2: Design Planning (Agent 2) ---
        print("[PIPELINE] Calling Agent 2 (Design Planner)...")
        design_plan = self.agent2.run(scene_data)

        # --- PHASE 3: Visualization (Agent 3) ---
        print("[PIPELINE] Calling Agent 3 (Visualizer & Guide)...")
        visual_output = self.agent3.run(scene_data, design_plan)
        print(f"[PIPELINE] Agent 3 Guide Length: {len(visual_output.get('guide', ''))}")
        print(f"[PIPELINE] Agent 3 Image Links: {visual_output.get('image_links')}")

        # --- PHASE 4: Procurement (Agent 4) ---
        print("[PIPELINE] Calling Agent 4 (Procurement Engine)...")
        try:
            # Ensure budget is an integer
            raw_budget = scene_data.get("budget", 30000)
            try:
                processed_budget = int(raw_budget)
            except:
                processed_budget = 30000

            procurement_plans = self.agent4.generate_comparison_plans(
                theme=scene_data.get("theme"),
                space_type=scene_data.get("space_type"),
                required_items=design_plan.get("required_items", []),
                user_budget=processed_budget
            )
            # Ensure we always have 3 plans
            if len(procurement_plans) < 3:
                print(f"[PIPELINE] Warning: Only {len(procurement_plans)} plans generated. Padding...")
                while len(procurement_plans) < 3:
                    procurement_plans.append({
                        "plan_name": f"Alternative Plan {len(procurement_plans)+1}",
                        "total_cost": 0,
                        "savings": scene_data.get("budget", 30000),
                        "items": []
                    })
        except Exception as e:
            print(f"[PIPELINE] Agent 4 Error: {e}")
            procurement_plans = [
                {"plan_name": "Luxury", "total_cost": 0, "savings": 0, "items": []},
                {"plan_name": "Moderate", "total_cost": 0, "savings": 0, "items": []},
                {"plan_name": "Minimal", "total_cost": 0, "savings": 0, "items": []}
            ]

        return {
            "status": "success",
            "is_iteration": bool(previous_scene),
            "project_id": os.urandom(4).hex(),
            "scene_analysis": scene_data,
            "design_strategy": {
                "summary": design_plan.get("design_summary"),
                "space_type": design_plan.get("space_type"),
                "theme": design_plan.get("theme")
            },
            "visuals": {
                "image_links": visual_output.get("image_links"),
                "transformation_guide": visual_output.get("guide"),
                "used_intensity": visual_output.get("visuals", {}).get("used_intensity", "moderate")
            },
            "procurement": {
                "comparison_plans": procurement_plans
            }
        }