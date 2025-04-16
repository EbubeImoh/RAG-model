import psycopg2
from config import DB_CONFIG  # Assuming DB_CONFIG is stored in a config file

def fetch_db_schema():
    try:
        conn = psycopg2.connect(**DB_CONFIG)  # Use DB_CONFIG to connect to the database
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name, column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Build schema string
        schema_dict = {}
        for table, column in rows:
            schema_dict.setdefault(table, []).append(column)

        schema_str = ""
        for table, columns in schema_dict.items():
            cols = ", ".join(columns)
            schema_str += f"Table {table} has columns: {cols}.\n"
        return schema_str.strip()
    except Exception as e:
        return f"Failed to fetch schema: {e}"