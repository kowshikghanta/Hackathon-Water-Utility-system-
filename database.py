import sqlite3

class Database:
    def __init__(self, database):
        self.database = database
        self.createtable()

    def createtable(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            flow_rate REAL,
            water_level REAL,
            leak_status INTEGER
        )
        ''')
        conn.commit()
        conn.close()

    def adduser(self, username, password):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

    def checkuser(self, username, password):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def getlatestdata(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10")
        data = cursor.fetchall()
        conn.close()
        return data
