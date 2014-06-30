import threading
from API import *
import random

random.seed(10)

count = 500
tag = Tags("benchmark.test8")
tag.addTag("sensorID", "benchmark.test11")
tag.addTag("sensorType", "benchmark")



#def work(count, seed, tag):
#    client = SensorClient()
#    for i in range(count):
#        for j in range(200):
#            client.pushToBuffer(1400000000 + int(j * seed * 100000), j, tag)
#        print client.batch()

#threadList = []
#for i in range(6):
#    t = threading.Thread(target = work, args = (count, random.random(), tag,))
#    threadList.append(t)

import time
start = time.time()

#client = SensorClient()
#for i in range(4000):
#    for j in range(50):
#        client.pushToBuffer(1400000000 + i * 50 + j, j, tag)
#    print client.batch()


import json
client = SensorClient()
data = client.singleQuery(1400000000, 1400000000 + 3999 * 50 + 49, tag)
end = time.time()
print "Used {0} s".format(end -start)
print len(json.loads(data)[0]["dps"])

#for thread in threadList:
#    thread.start()

#for thread in threadList:
#    thread.join()


