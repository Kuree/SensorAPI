from Configuration import *
import json
import requests
import time

class SensorAPI:
    def __init__(self):
        '''
        '''
        self.config = Configuration()

    def computeMetrics(self, timestamp, value):
        metric = self.config.location
        tags = {"sensorID": self.config.sensorID, "sensorType": self.config.sensorType}
        return {'metric': metric, 'timestamp': timestamp, 'value': value, 'tags' : tags}

    def put(self, timestamp, value):
        url = 'http://{0}:{1}/api/put'.format(self.config.host, self.config.port)
        tsdbMetrics = self.computeMetrics(timestamp, value)
        return self.postRequest(url, tsdbMetrics)

    def postRequest(self, url, requestData):
        try:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(url, data=json.dumps(requestData), headers=headers)
            return True
        except:
            return False

    def batch(self, dic):
        url = 'http://{0}:{1}/api/put'.format(self.config.host, self.config.port)
        tsdbMetrics = []
        for k in dic:
            tsdbMetrics += [self.computeMetrics(k, dic[k])]
        return self.postRequest(url, tsdbMetrics)


    def __query(self, start, end, queries, aggregators):
        
        url = 'http://{0}:{1}/api/query'.format(self.config.host, self.config.port)
        tsdbMetrics = {
            "start" : start,
            "end" : end,
            "queries" : queries
            }
        return self.postRequest(url, tsdbMetrics)

    def __query(self, start, queries):
        
        self.singleQuery(start, end, queries)

    def singleQuery(self ,start, location, sensorID):
        queries = [
            {
                "metric":location,
                "tags": sensorID
            }]
        self.singleQuery(start, location, queries)

    