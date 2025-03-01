import serial
import sqlite3
import time
import modules.utils
from modules.sensors import processsensordata
try:
    arduino = serial.Serial("COM5", 9600, timeout=1)
    print("Connected to Arduino")
except serial.SerialException:
    print("Error: Could not connect to Arduino")
    arduino = None

def readarduino():
    if not arduino:
        return
    while True:
        try:
            data = arduino.readline().decode().strip()
            if data:
                values = data.split(",")
                if len(values) == 2:
                    flowrate, waterlevel = map(float, values)
                    print(flowrate,waterlevel)
                    processsensordata(flowrate, waterlevel)
        except Exception as e:
            print(f"Error reading Arduino: {e}")
        time.sleep(2)

if __name__ == "__main__":
    readarduino()