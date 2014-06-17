import ConfigParser
from Query import *
from Put import *
import json
import requests
import time
import logging
from ZeroMQLayer import ZeroMQClient
import os

class _ClientConf(object):
    def __init__(self):
        self.conf = ConfigParser.ConfigParser()
        if os.path.isfile("client.conf"):
            self.conf.read("client.conf")
            logging.info("Using configuration file at client.conf")
        else:
            self.conf.set("ZeroMQQueueServer", "ServerIP", "localhost")
            self.conf.set("ZeroMQQueueServer", "ServerPort", 5555)
            logging.warn("Could not find client.conf. Use default setting now")

    def getQueueHost(self):
        return self.conf.get("ZeroMQQueueServer", "ServerIP")
    def getQueuePort(self):
        return self.conf.get("ZeroMQQueueServer", "ServerPort")


class SensorAPI(ZeroMQClient.Client):
    '''API that dealing with web request with OpenTSDB'''
    def __init__(self):
        '''
        Initialize the sensor API with Configuration file as the API needs to know the request address and port
        It is recommended to use SensorClient in stead of SensorAPI for flexibility

        conf: API.Configuration
        '''
        super(SensorAPI, self).__init__()
        self._conf = _ClientConf()
        self.logger = logging.getLogger("SensorAPI_API")
        self.SERVER_ENDPOINT = "tcp://{0}:{1}".format(self._conf.getQueueHost(), self._conf.getQueuePort())
        self._connect()
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
        #url = 'http://{0}:{1}'.format(self.config.getHost(), self.config.getPort())
        return self.__postRequest("put", datas)

    def singlePut(self, putData):
        '''
        Put single data point into OpenTSDB.
        Returns feedback for a single put in JSON

        data: API.PutData
        '''
        return self.multiplePut([putData])

    def __postRequest(self, method, requestData):
        '''
        Basic web request function for Sensor API
        Returns web request response if success; otherwise returns exception message
        
        url: string
        requestData: Dictionary structure. The function itself will dump the dictionary to JSON for you
        '''
        try:
            # headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            jsonData = { "method" : method,
                        "data": requestData}
            #r = requests.post(url, data=json.dumps(jsonData) , headers=headers)
            #return r.text
            return self._sendData(jsonData)
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
        #url = 'http://{0}:{1}'.format(self.config.getHost(), self.config.getPort())
        return self.__postRequest("query", queryData)

    
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


        #url = url = 'http://{0}:{1}'.format(self.config.getHost(), self.config.getPort())

        return self.__postRequest("querylast", queryLastData)
        pass