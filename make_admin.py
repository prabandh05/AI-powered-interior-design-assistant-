import sys
from app import app, db, User

def set_admin(username):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            user.is_admin = True
            db.session.commit()
            print(f"Success: {username} is now an admin!")
        else:
            print(f"Error: User '{username}' not found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python make_admin.py <username>")
    else:
        set_admin(sys.argv[1])
