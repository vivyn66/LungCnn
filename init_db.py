import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import App
except Exception as e:
    print(f"[FAIL] Failed to import App configurations: {e}")
    sys.exit(1)

def initialize_database():
    print("Connecting to remote database using App configuration...")
    try:
        conn = App.get_db_connection()
        cursor = conn.cursor()
    except Exception as e:
        print(f"[FAIL] Database connection failed: {e}")
        print("Please check your environment variables (DB_HOST, DB_USER, DB_PASSWORD, etc.).")
        sys.exit(1)

    print("Connection established. Reading schema.sql...")
    schema_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')
    if not os.path.exists(schema_file):
        print(f"[FAIL] schema.sql not found at: {schema_file}")
        sys.exit(1)

    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    # Split SQL by semicolons to execute statement-by-statement
    # Note: simple splitting works as schema.sql doesn't have complex procedural triggers/routines
    statements = schema_sql.split(';')
    success_count = 0
    fail_count = 0

    print("Executing initialization statements...")
    for stmt in statements:
        stmt = stmt.strip()
        if not stmt:
            continue
        try:
            cursor.execute(stmt)
            success_count += 1
        except Exception as e:
            print(f"[WARN] Failed to execute statement: {stmt[:50]}... Error: {e}")
            fail_count += 1

    try:
        conn.commit()
        cursor.close()
        conn.close()
        print(f"\n[PASS] Database schema initialization completed successfully.")
        print(f"       Statements executed successfully: {success_count}")
        print(f"       Statements skipped/failed: {fail_count}")
    except Exception as e:
        print(f"[FAIL] Transaction commit failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    initialize_database()
