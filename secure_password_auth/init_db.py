import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "db" / "users.db"
DB.parent.mkdir(exist_ok=True)

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    event TEXT,
    ip TEXT,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
print(f"Initialised DB at: {DB}")
