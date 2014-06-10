from Client import *
import json

# create configuration for sensor client
conf = Configuration()

# create a sensor client
client = SensorClient(conf)

# create individual tags
# tags should not have spaces
tags1 = Tags(conf, "bucknell.dana")
tags1.addTag("sensorID", "1234")
tags1.addTag("sensorType", "type1")

tags2 = Tags(conf, "bucknell.aw")
tags2.addTag("sensorID", "5678")
tags2.addTag("sensorID", "type2")

## put function will return a state string
#print client.singlePut(client.now(), 1, tags1)
#print client.singlePut(client.now(), 2, tags1)


# multiple put
data = []
for i in range(10):
    time.sleep(0.01) # some work to fetch data
    data += [(client.nowMS(), i, tags1)]
print client.multiplePut(data)


# query data
start = client.nowMS() - 2000000
print client.singleQuery(start, client.nowMS(), tags1)


# query last put
#print client.singleQueryLast(tags1)



# batch data
# Not working right now
#client.pushToBuffer(client.now(), 1, tags1)
#client.pushToBuffer(client.now(), 2, tags1)
#print client.batch()
