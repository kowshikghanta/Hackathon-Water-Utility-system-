import sqlite3
from modules.utils import getdbconnection
def processsensordata(flowrate, waterlevel):
    leakstatus = 1 if abs(flowrate - waterlevel) > (flowrate * 0.05) else 0  # 5% threshold
    savetodatabase(flowrate, waterlevel, leakstatus)
    return leakstatus

def savetodatabase(flowrate, waterlevel, leakstatus):
    conn = getdbconnection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        flowrate REAL NOT NULL,
                        waterlevel REAL NOT NULL,
                        leakstatus INTEGER NOT NULL CHECK (leakstatus IN (0,1))
                        )''')
    cursor.execute('''
        INSERT INTO sensor_data (flowrate, waterlevel, leakstatus)
        VALUES (?, ?, ?)
    ''', (flowrate, waterlevel, leakstatus))
    conn.commit()
    conn.close()
