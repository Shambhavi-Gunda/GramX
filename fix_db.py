import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE posts ADD COLUMN user_id TEXT;")
    conn.commit()
    print("✅ user_id column added successfully")
except Exception as e:
    print("⚠️", e)

conn.close()
