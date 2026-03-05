import sqlite3

DATABASE_NAME = "trustlens.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT,
    image_hash TEXT,
    damage_type TEXT,
    severity_score REAL,
    explanation TEXT,
    base_price REAL,
    final_price REAL
)
    """)

    conn.commit()
    conn.close()
