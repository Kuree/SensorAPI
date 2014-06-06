import Configuration
from Query import *
from Put import *
import json
import requests
import time

class SensorAPI:
    def __init__(self, conf):
        self.config = conf
        pass

    
    
    def multiplePut(self, putDatas):
        url = 'http://{0}:{1}/api/put?details'.format(self.config.getHost(), self.config.getPort())
        return self.postRequest(url, putDatas)

   
    def singlePut(self, timestamp, value, tags):
        data = PutData(timestamp, value, tags)
        return self.multiplePut([data.toPutData()])

    def postRequest(self, url, requestData):
        try:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(requestData), headers=headers)
            return r.text
        except Exception as e:
            return e.message
        
    def batch(self, dic):
        url = 'http://{0}:{1}/api/put?'.format(self.config.getHost(), self.config.getPort())
        tsdbMetrics = []
        for k in dic:
            tsdbMetrics += [self.computeMetrics(k, dic[k])]
        return self.postRequest(url, tsdbMetrics)


    def multipleQuery(self, start, end, queries):
        queryData = {}
        queryData["start"] = start
        queryData["end"] = end
        queryData["queries"] = queries
        url = 'http://{0}:{1}/api/query'.format(self.config.getHost(), self.config.getPort())
        return self.postRequest(url, queryData)

    
    def singleQuery(self, start, end, tags):
        query = QueryData(tags)
        print query.toQueryData()
        return self.multipleQuery(start, end, [query.toQueryData()])

    def now(self):
        return int(round(time.time() * 1000))