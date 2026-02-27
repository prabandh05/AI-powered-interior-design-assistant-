import sqlite3
import os

def visualize_schema():
    db_path = os.path.join('instance', 'users.db')
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("\n" + "="*60)
    print("           GRUHA ASSISTANT - DATABASE SCHEMA")
    print("="*60)

    for table_name_tuple in tables:
        table_name = table_name_tuple[0]
        if table_name == 'sqlite_sequence':
            continue
            
        print(f"\n[ TABLE: {table_name.upper()} ]")
        print("-" * 60)
        print(f"{'Column Name':<20} | {'Type':<15} | {'Nullable':<10} | {'PK'}")
        print("-" * 60)

        # Get column info: cid, name, type, notnull, dflt_value, pk
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        for col in columns:
            cid, name, col_type, notnull, dflt, pk = col
            nullable = "No" if notnull else "Yes"
            primary_key = "Yes" if pk else ""
            print(f"{name:<20} | {col_type:<15} | {nullable:<10} | {primary_key}")
        
        # Get Foreign Keys
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        fks = cursor.fetchall()
        if fks:
            print(f"\nForeign Keys:")
            for fk in fks:
                # id, seq, table, from, to, on_update, on_delete, match
                print(f"  - {fk[3]} -> {fk[2]}({fk[4]})")
        
        print("-" * 60)

    conn.close()

if __name__ == "__main__":
    visualize_schema()
