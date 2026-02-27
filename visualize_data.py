import sqlite3
import os
from datetime import datetime

def visualize_data():
    try:
        from tabulate import tabulate
    except ImportError:
        print("Error: 'tabulate' library not found. Please run 'pip install tabulate'")
        return

    db_path = os.path.join('instance', 'users.db')
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return

    # Prepare timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"db_snapshot_{timestamp}.txt"
    filepath = os.path.join('instance', filename)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    output_lines = []
    output_lines.append("\n" + "="*80)
    output_lines.append("           GRUHA ASSISTANT - REAL-TIME DATABASE EXPLORER")
    output_lines.append("="*80)

    for table_name_tuple in tables:
        table_name = table_name_tuple[0]
        if table_name == 'sqlite_sequence':
            continue
            
        output_lines.append(f"\n>>> [ TABLE: {table_name.upper()} ]")
        
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [col[1] for col in cursor.fetchall()]
        
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100;")
        rows = cursor.fetchall()
        
        if not rows:
            output_lines.append(" (Table is currently empty)")
            continue

        formatted_rows = []
        for row in rows:
            formatted_row = list(row)
            if table_name.lower() == 'user':
                try:
                    pwd_idx = columns.index('password_hash')
                    formatted_row[pwd_idx] = "********"
                except ValueError:
                    pass
            
            for i, val in enumerate(formatted_row):
                if isinstance(val, str) and len(val) > 20:
                    formatted_row[i] = val[:17] + "..."
            
            formatted_rows.append(formatted_row)

        table_str = tabulate(formatted_rows, headers=columns, tablefmt="presto")
        output_lines.append(table_str)
        
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        total_count = cursor.fetchone()[0]
        output_lines.append(f"\nShowing {len(rows)} of {total_count} records")
        output_lines.append("-" * 80)

    conn.close()

    # Final Output to Console and File
    final_output = "\n".join(output_lines)
    print(final_output)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_output)
    
    print(f"\n✅ Output also saved to: {filepath}")

if __name__ == "__main__":
    visualize_data()
