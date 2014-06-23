import threading
from API import *
import random

random.seed(10)

count = 500
tag = Tags("benchmark.test6")
tag.addTag("sensorID", "benchmark.test9")
tag.addTag("sensorType", "benchmark")



def work(count, seed, tag):
    client = SensorClient()
    for i in range(count):
        for j in range(200):
            client.pushToBuffer(1400000000 + int(j * seed * 100000), j, tag)
        print client.batch()

threadList = []
for i in range(6):
    t = threading.Thread(target = work, args = (count, random.random(), tag,))
    threadList.append(t)


import time
start = time.time()


for thread in threadList:
    thread.start()

for thread in threadList:
    thread.join()

end = time.time()
print "Used {0} s".format(end -start)