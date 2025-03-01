import sqlite3 as siri
conn=siri.connect("utility_data.db")
data=conn.execute('select * from sensor_data')
for row in data:
    print(row[0],row[1],row[2],row[3])
conn.close()