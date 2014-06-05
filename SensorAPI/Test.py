from API import *
import time
import random
api = SensorAPI()
timestamp = int(round(time.time() - 100000000) * 1000)

#for i in range(100):
#    time.sleep(0.01)
#    print api.singlePut(api.now(), 10 +random.randint(10, 20))
#time.sleep(10)
print api.singleQuery(start = timestamp, location = "unknown", sensorID = "37109", sensorType = "37109")