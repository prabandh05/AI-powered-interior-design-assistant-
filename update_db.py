import sqlite3
import os

db_path = os.path.join('instance', 'users.db')
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the column exists
        cursor.execute("PRAGMA table_info(design_history)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if "procurement_plans_json" not in columns:
            print("Adding column procurement_plans_json to design_history...")
            cursor.execute("ALTER TABLE design_history ADD COLUMN procurement_plans_json TEXT")
            conn.commit()
            print("Successfully updated database schema.")
        else:
            print("Column procurement_plans_json already exists.")
            
        conn.close()
    except Exception as e:
        print(f"Error updating database: {e}")
else:
    print(f"Database not found at {db_path}")
