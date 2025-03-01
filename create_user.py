import sqlite3

conn = sqlite3.connect("data/utility_data.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

conn.execute("""
INSERT INTO users (username, password) VALUES ("kowshik", "kowshik1234")
""")
conn.commit()
conn.close()