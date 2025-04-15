import psycopg2
from config.db_config import DB_CONFIG

def load_schema():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)
    schema = cur.fetchall()
    cur.close()
    conn.close()
    return schema
