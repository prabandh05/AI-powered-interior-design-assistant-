from typing import List, Dict, Any


class Agent4ProcurementEngine:

    def __init__(self, dataset: Dict[str, Any]):
        self.items = dataset["items"]
        self.price_ranges = dataset["metadata"]["price_ranges_inr"]

    # --------------------------------------------------
    # FILTERING WITH LAYERED FALLBACK
    # --------------------------------------------------

    def filter_items(self, theme, space_type, item_type):

        # Strict: theme + space
        results = [
            item for item in self.items
            if item["item_type"] == item_type
            and theme in item["themes"]
            and space_type in item.get("space_types", [])
            and not item["is_diy"]
        ]
        if results:
            return results

        # Relaxed: theme only
        results = [
            item for item in self.items
            if item["item_type"] == item_type
            and theme in item["themes"]
            and not item["is_diy"]
        ]
        if results:
            return results

        # Last fallback: item_type only
        return [
            item for item in self.items
            if item["item_type"] == item_type
            and not item["is_diy"]
        ]

    def get_diy_items(self, theme, item_type):
        return [
            item for item in self.items
            if item["item_type"] == item_type
            and theme in item["themes"]
            and item["is_diy"]
        ]

    # --------------------------------------------------
    # PRICE CLASSIFICATION
    # --------------------------------------------------

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

    # --------------------------------------------------
    # ESTIMATE MINIMUM REMAINING COST
    # --------------------------------------------------

    def estimate_min_remaining_cost(self, theme, space_type, remaining_item_types):
        cost = 0
        for item_type in remaining_item_types:
            candidates = self.filter_items(theme, space_type, item_type)
            buckets = self.classify_by_price_range(candidates)
            cheapest = self.select_cheapest(buckets["low"])
            if cheapest:
                cost += cheapest["price"]
        return cost

    # --------------------------------------------------
    # BUILD PLAN (PRIORITY AWARE)
    # --------------------------------------------------

    def build_plan(
        self,
        theme: str,
        space_type: str,
        required_items: List[Dict],
        target_budget: int,
        tier_order: List[str]
    ):

        # 🔥 Sort by priority
        required_items = sorted(required_items, key=lambda x: x["priority"])
        required_item_types = [item["item_type"] for item in required_items]

        plan_items = []
        total_cost = 0

        for idx, item_type in enumerate(required_item_types):
            remaining_item_types = required_item_types[idx + 1:]

            candidates = self.filter_items(theme, space_type, item_type)
            buckets = self.classify_by_price_range(candidates)

            selected_item = None

            min_remaining_cost = self.estimate_min_remaining_cost(
                theme, space_type, remaining_item_types
            )

            for tier in tier_order:
                candidate = self.select_cheapest(buckets[tier])
                if candidate:
                    projected_cost = (
                        total_cost + candidate["price"] + min_remaining_cost
                    )
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

    # --------------------------------------------------
    # GENERATE MULTIPLE COMPARISON PLANS
    # --------------------------------------------------

    def generate_comparison_plans(
        self,
        theme: str,
        space_type: str,
        required_items: List[Dict],
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


# --------------------------------------------------
# TEST RUN
# --------------------------------------------------

if __name__ == "__main__":

    print("Agent 4 is running (Priority Aware) ✅")

    import os, json

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATASET_PATH = os.path.join(BASE_DIR, "dataset", "indian_interior_v2.json")

    with open(DATASET_PATH) as f:
        dataset = json.load(f)

    engine = Agent4ProcurementEngine(dataset)

    required_items = [
        {"item_type": "study_table", "priority": 1},
        {"item_type": "curtains", "priority": 2},
        {"item_type": "ceiling_light", "priority": 3}
    ]

    plans = engine.generate_comparison_plans(
        theme="rajasthani_mughal",
        space_type="study_room",
        required_items=required_items,
        user_budget=50000
    )

    print(json.dumps(plans, indent=2))