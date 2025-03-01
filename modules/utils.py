import sqlite3

def getdbconnection():
    return sqlite3.connect("data/utility_data.db", check_same_thread=False)

