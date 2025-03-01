import sqlite3
from modules.utils import getdbconnection

def checklogin(username, password):
    conn = getdbconnection()
    user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
    conn.close()
    return user is not None

