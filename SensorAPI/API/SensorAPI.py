import Configuration
from Query import *
from Put import *
import json
import requests
import time

class SensorAPI:
    def __init__(self):
        self.config = Configuration.Configuration()
        pass

    def computeMetrics(self, timestamp, value):
        metric = self.config.location
        tags = {"sensorID": self.config.sensorID, "sensorType": self.config.sensorType}
        return {'metric': metric, 'timestamp': timestamp, 'value': value, 'tags' : tags}

    #def put(self, timestamp = int(round(time.time() * 1000)), value = 0):
    #    url = 'http://{0}:{1}/api/put'.format(self.config.host, self.config.port)
    #    tsdbMetrics = self.computeMetrics(timestamp, value)
    #    return self.postRequest(url, tsdbMetrics)

    
    
    def multiplePut(self, putDatas):
        url = 'http://{0}:{1}/api/put?details'.format(self.config.host, self.config.port)
        return self.postRequest(url, putDatas)

   
    def singlePut(self, timestamp = int(round(time.time() * 1000)), value = 0, conf = Configuration.Configuration()):
        data = PutData(timestamp=timestamp, value = value, conf = conf)
        return self.multiplePut([data.toPutData()])


    def postRequest(self, url, requestData):
        try:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(requestData), headers=headers)
            return r.text
        except Exception as e:
            return e.message
        
    def batch(self, dic):
        url = 'http://{0}:{1}/api/put?'.format(self.config.host, self.config.port)
        tsdbMetrics = []
        for k in dic:
            tsdbMetrics += [self.computeMetrics(k, dic[k])]
        return self.postRequest(url, tsdbMetrics)


    def multipleQuery(self, start, end, queries):
        queryData = {}
        queryData["start"] = start
        queryData["end"] = end
        queryData["queries"] = queries
        url = 'http://{0}:{1}/api/query'.format(self.config.host, self.config.port)
        return self.postRequest(url, queryData)

    
    def singleQuery(self, start = int(round(time.time()*1000 - 2000)), end = int(round(time.time() * 1000)), 
                    location = "Unknown", sensorID = "Unknown", sensorType = "Unknown"):
        query = QueryData(location = location, sensorID = sensorID, sensorType = sensorType)
        print query.toQueryData()
        return self.multipleQuery(start, end, [query.toQueryData()])

    def now(self):
        return int(round(time.time() * 1000))