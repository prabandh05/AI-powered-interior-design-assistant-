from app import app, db, User, DesignHistory
from flask_bcrypt import Bcrypt
import random
from datetime import datetime, timedelta

bcrypt = Bcrypt()

def seed():
    with app.app_context():
        # Clear existing data optionally? No, let's just add.
        # But for 50+ fresh records, maybe clear is better for a clean demo.
        print("Dropping and recreating all tables...")
        db.drop_all()
        db.create_all()
        db.session.commit()

        print("Creating admin user...")
        admin_pass = "12345678"
        admin = User(
            name="Platform Admin",
            username="admin",
            email="admin@gruha.com",
            password_hash=bcrypt.generate_password_hash(admin_pass).decode('utf-8'),
            location="Bangalore, KA",
            is_admin=True
        )
        db.session.add(admin)

        print("Creating dummy users...")
        locations = ["Mumbai, MH", "Delhi, DL", "Bangalore, KA", "Hyderabad, TG", "Chennai, TN", "Kolkata, WB", "Pune, MH", "Jaipur, RJ"]
        users = []
        for i in range(1, 11):
            user = User(
                name=f"User {i}",
                username=f"user{i}",
                email=f"user{i}@example.com",
                password_hash=bcrypt.generate_password_hash("password123").decode('utf-8'),
                location=random.choice(locations),
                is_admin=False
            )
            users.append(user)
            db.session.add(user)
        
        db.session.commit()

        print("Generating 60 design history records...")
        themes = ["traditional_indian", "contemporary_indian", "rustic_indian", "rajasthani_mughal"]
        spaces = ["living_room", "bedroom", "kitchen", "study_room"]
        plans = ["Minimal", "Moderate", "Luxury"]
        
        # Start time 30 days ago
        base_time = datetime.utcnow() - timedelta(days=30)

        for i in range(60):
            # Pick a random user
            user = random.choice(users)
            history_budget = random.choice([25000, 60000, 100000, 150000])
            
            # Spread out the time
            # Some designs in the past month, roughly 2 per day
            record_time = base_time + timedelta(days=i // 2, hours=random.randint(0, 23))
            
            intensity = "minimal"
            if history_budget > 25000: intensity = "moderate"
            if history_budget > 60000: intensity = "luxury"

            history = DesignHistory(
                user_id=user.id,
                theme=random.choice(themes),
                space_type=random.choice(spaces),
                budget=history_budget,
                total_cost=random.randint(15000, 140000),
                selected_plan=random.choice(plans),
                design_intensity=intensity,
                image_url=f"http://127.0.0.1:8000/images/design_seed_{i}.png",
                procurement_plans_json=json.dumps([
                    {
                        "plan_name": "Luxury",
                        "total_cost": history_budget,
                        "savings": 0,
                        "items": [{"item_type": "Gold Filtered Item", "selection": "Premium Selection", "price": history_budget, "link": "#"}]
                    },
                    {
                        "plan_name": "Moderate",
                        "total_cost": int(history_budget * 0.7),
                        "savings": int(history_budget * 0.3),
                        "items": [{"item_type": "Silver Filtered Item", "selection": "Balanced Selection", "price": int(history_budget * 0.7), "link": "#"}]
                    },
                    {
                        "plan_name": "Minimal",
                        "total_cost": int(history_budget * 0.5),
                        "savings": int(history_budget * 0.5),
                        "items": [{"item_type": "Bronze Filtered Item", "selection": "Essential Selection", "price": int(history_budget * 0.5), "link": "#"}]
                    }
                ]),
                created_at=record_time
            )
            db.session.add(history)
        
        db.session.commit()
        print(f"Successfully seeded database!")
        print(f"Admin Username: admin | Password: {admin_pass}")

if __name__ == "__main__":
    seed()
