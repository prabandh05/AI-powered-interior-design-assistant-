from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to history
    designs = db.relationship('DesignHistory', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class DesignHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    theme = db.Column(db.String(50))
    space_type = db.Column(db.String(50))
    budget = db.Column(db.Integer)
    total_cost = db.Column(db.Integer)
    # Selected procurement plan (e.g., "Luxury", "Moderate", "Minimal")
    selected_plan = db.Column(db.String(100))
    # Visualization richness/tier (minimal, moderate, luxury)
    design_intensity = db.Column(db.String(50))
    # Path to the generated image if saved locally
    image_url = db.Column(db.String(255))
    procurement_plans_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Design {self.id} for User {self.user_id}>'
