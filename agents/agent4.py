from typing import List, Dict


class Agent4ProcurementEngine:
    def __init__(self, dataset: Dict):
        self.items = dataset["items"]
        self.price_ranges = dataset["metadata"]["price_ranges_inr"]

    # -------------------------
    # FILTERING
    # -------------------------
    def filter_items(self, theme, space_type, item_type, strict=True):
        results = [
            item for item in self.items
            if item["item_type"] == item_type
            and theme in item["themes"]
            and not item["is_diy"]
        ]
        if strict:
            results = [
                item for item in results
                if space_type in item.get("space_types", [])
            ]
        return results

    def get_diy_items(self, theme, item_type):
        return [
            item for item in self.items
            if item["item_type"] == item_type
            and theme in item["themes"]
            and item["is_diy"]
        ]

    # -------------------------
    # PRICE CLASSIFICATION
    # -------------------------
    def classify_by_price_range(self, items):
        buckets = {"low": [], "medium": [], "premium": []}
        for item in items:
            for tier, limits in self.price_ranges.items():
                if tier == "diy":
                    continue
                if limits["min"] <= item["price"] <= limits["max"]:
                    buckets[tier].append(item)
                    break
        return buckets

    def select_cheapest(self, items):
        return sorted(items, key=lambda x: x["price"])[0] if items else None

    # -------------------------
    # MINIMUM COST ESTIMATION
    # -------------------------
    def estimate_min_remaining_cost(self, theme, space_type, remaining_items):
        cost = 0
        for item_type in remaining_items:
            candidates = self.filter_items(theme, space_type, item_type)
            buckets = self.classify_by_price_range(candidates)
            cheapest = self.select_cheapest(buckets["low"])
            if cheapest:
                cost += cheapest["price"]
        return cost

    # -------------------------
    # BUILD PLAN (UPGRADED)
    # -------------------------
    def build_plan(self, theme, space_type, required_items, target_budget, tier_order):
        plan_items = []
        total_cost = 0

        for idx, item_type in enumerate(required_items):
            remaining_items = required_items[idx + 1:]

            candidates = self.filter_items(theme, space_type, item_type)
            if not candidates:
                candidates = self.filter_items(theme, space_type, item_type, strict=False)

            buckets = self.classify_by_price_range(candidates)
            selected_item = None

            min_remaining_cost = self.estimate_min_remaining_cost(
                theme, space_type, remaining_items
            )

            for tier in tier_order:
                candidate = self.select_cheapest(buckets[tier])
                if candidate:
                    projected_cost = total_cost + candidate["price"] + min_remaining_cost
                    if projected_cost <= target_budget:
                        selected_item = candidate
                        break

            if not selected_item:
                diy = self.get_diy_items(theme, item_type)
                plan_items.append({
                    "item_type": item_type,
                    "selection": "DIY",
                    "price": 0,
                    "link": diy[0]["diy_link"] if diy else None
                })
                continue

            total_cost += selected_item["price"]
            plan_items.append({
                "item_type": item_type,
                "selection": selected_item["name"],
                "price": selected_item["price"],
                "quality_level": selected_item["quality_level"],
                "link": selected_item["product_link"]
            })

        return {
            "total_cost": total_cost,
            "savings": target_budget - total_cost,
            "items": plan_items
        }

    # -------------------------
    # GENERATE PLANS
    # -------------------------
    def generate_comparison_plans(
        self,
        theme: str,
        space_type: str,
        required_items: List[str],
        user_budget: int
    ):
        budget_targets = [
            user_budget,
            int(user_budget * 0.7),
            int(user_budget * 0.5)
        ]

        tier_preferences = [
            ["premium", "medium", "low"],
            ["medium", "low"],
            ["low"]
        ]

        plans = []
        for i, (budget, tiers) in enumerate(zip(budget_targets, tier_preferences), 1):
            plan = self.build_plan(theme, space_type, required_items, budget, tiers)
            plan["plan_name"] = f"Plan {i}"
            plan["budget_limit"] = budget
            plans.append(plan)

        return plans


# -------------------------
# TEST RUN
# -------------------------
if __name__ == "__main__":
    print("Agent 4 is running ✅")

    import os, json

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATASET_PATH = os.path.join(BASE_DIR, "dataset", "indian_interior_v2.json")

    with open(DATASET_PATH) as f:
        dataset = json.load(f)

    engine = Agent4ProcurementEngine(dataset)

    plans = engine.generate_comparison_plans(
        theme="rajasthani_mughal",
        space_type="study_room",
        required_items=["study_table", "curtains", "ceiling_light"],
        user_budget=50000
    )

    print(json.dumps(plans, indent=2))