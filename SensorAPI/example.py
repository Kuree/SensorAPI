from Client import *
# create configuration for sensor client
conf = Configuration()

# add tags to configuration
conf.addTag("sensorID")
conf.addTag("sensorType")

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

# put function will return a state string
print client.singlePut(1, tags1, timestamp = client.now())
print client.singlePut(2, tags2, timestamp = client.now())

# query data
start = client.now() - 2000000
print client.singleQuery(start, client.now(), tags1)


#print QueryAggregator.Sum
