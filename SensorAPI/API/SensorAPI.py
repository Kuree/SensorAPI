import Configuration
from Query import *
from Put import *
import json
import requests
import time
import logging

class SensorAPI(object):
    '''API that dealing with web request with OpenTSDB'''
    def __init__(self, conf):
        '''
        Initialize the sensor API with Configuration file as the API needs to know the request address and port
        It is recommended to use SensorClient in stead of SensorAPI for flexibility

        conf: API.Configuration
        '''
        self.config = conf
        self.logger = logging.getLogger("SensorAPI_API")
        return
    
    def multiplePut(self, putDatas):
        '''
        Put multiple data points into OpenTSDB
        Returns multiple feedback in JSON

        putDatas: list<PutData>
        '''
        datas = []

        self.logger.info("Put data count: {0}".format(len(putDatas)))
        if self.logger.isEnabledFor(logging.DEBUG):
            for data in putDatas:
                self.logger.debug("PutData: {0}".format(data))

        for d in putDatas:
            datas += [d.toPutData()]
        url = 'http://{0}:{1}'.format(self.config.getHost(), self.config.getPort())
        return self.__postRequest(url, "put", datas)

    def singlePut(self, putData):
        '''
        Put single data point into OpenTSDB.
        Returns feedback for a single put in JSON

        data: API.PutData
        '''
        return self.multiplePut([putData])

    def __postRequest(self, url, method, requestData):
        '''
        Basic web request function for Sensor API
        Returns web request response if success; otherwise returns exception message
        
        url: string
        requestData: Dictionary structure. The function itself will dump the dictionary to JSON for you
        '''
        try:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            jsonData = { method : [requestData]}
            r = requests.post(url, data=json.dumps(jsonData) , headers=headers)
            return r.text
        except Exception as e:
            return e.message


    def multipleQuery(self, start, end, queries):
        '''
        Query the OpenTSDB server with start and end time with multiple query data
        Returns JSON data correspond to given query data

        start: start timestamp to query. Standard int in millisecond precision.
        end: end timestamp to query. Standard int in millisecond precision.
        queries: list<QueryData>
        '''
        self.logger.info("Query Info: start: {0}, end: {1}, query count: {0}".format(start, end, len(queries)))
        if self.logger.isEnabledFor(logging.DEBUG):
            for query in queries:
                self.logger.debug("QueryData: {0}".format(query))

        queryData = {}
        queryData["start"] = start
        queryData["end"] = end
        data = []
        for query in queries:
            data += [query.toQueryData()]
        queryData["queries"] = data
        url = 'http://{0}:{1}'.format(self.config.getHost(), self.config.getPort())
        return self.__postRequest(url, "query", queryData)

    
    def singleQuery(self, start, end, queryData):
        '''
        Query the OpenTSDB server with start and end time.
        Returns JSON data correspond to given query data

        start: start timestamp to query. Standard int in millisecond precision.
        end: end timestamp to query. Standard int in millisecond precision.
        queryData: QueryData
        '''
        return self.multipleQuery(start, end, [queryData])

    def singleQueryLast(self, queryLast):
        return self.multipleQueryLast([queryLast])

    def multipleQueryLast(self, queryLastList):

        queryLastData = {}
        data = []
        for queryLast in queryLastList:
            data += [queryLast.toQueryData()]
        queryLastData["queries"] = data


        url = url = 'http://{0}:{1}'.format(self.config.getHost(), self.config.getPort())

        return self.__postRequest(url, "querylast", queryLastData)
        pass