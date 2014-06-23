from API.SensorClient import *
import json
import requests
import logging
import sys

# set up logging
#logger = logging.getLogger("SensorAPI_API")
#logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.DEBUG)

# create a sensor client
client = SensorClient()

# create individual tags
# tags should not have spaces
tags1 = Tags("bucknell.dana.test04")
tags1.addTag("sensorID", "1234")
tags1.addTag("sensorType", "type1")

tags2 = Tags("bucknell.aw")
tags2.addTag("sensorID", "5678")
tags2.addTag("sensorID", "type2")

## put function will return a state string
#print client.singlePut(client.nowMS(), 1, tags1)
#print client.singlePut(client.nowMS(), 2, tags1)


# multiple put
#data = []
#m = 0
#t = client.nowS()
#for j in range(10):
#    for i in range(1000):
#        #time.sleep(0.01) # some work to fetch data
#        data += [(t - 1000000 + m, i, tags1)]
#        m += 1
#    print client.multiplePut(data)
#    data = []


## query data
start = client.nowS() - 10000000 # fake a start time
print len(json.loads(client.singleQuery(start, client.nowS(), tags1))[0]["dps"])




## query last put
## OpenTSDB 2.0 does not support query last
## Waiting for 2.1
##print client.singleQueryLast(tags1)



## batch data

#for i in range(1000):
#    client.pushToBuffer(client.nowS() - 1000 * i, i, tags1)
#print client.batch()
