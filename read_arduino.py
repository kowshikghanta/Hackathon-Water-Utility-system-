import random
import time
from modules.sensors import processsensordata

def simulatesensordata():
    while True:
        flowrate = round(random.uniform(10, 50), 2)
        waterlevel = round(random.uniform(0, 100), 2)

        print(f"Simulated Data -> Flowrate: {flowrate} L/min, Water Level: {waterlevel} cm")
        
        processsensordata(flowrate, waterlevel)

        time.sleep(2)

if __name__ == "__main__":
    simulatesensordata()
