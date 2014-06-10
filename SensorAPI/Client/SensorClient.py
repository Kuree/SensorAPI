from API import *
import Queue
import time
class SensorClient:
    '''An easy to use sensor client for OpenTSDB'''

    def pushToBuffer(self, value, tags, timestamp = None):
        if timestamp == None: timestamp = self.now()
        self.__queue.put(PutData(timestamp, value, tags))
        self.__queue.task_done()


    def batch(self):
        putDatas = []
        #for data in iter(self.__queue.get, "STOP"):
        #    putDatas.append(data)
        while not self.__queue.empty():
            putDatas.append(self.__queue.get())
        self.__queue.join()
        return self.api.multiplePut(putDatas)
        

    def __init__(self, conf):
        '''
        Initialize the sensor client with given configuration

        conf: Client.Configuration
        '''
        self.conf = conf
        self.api = SensorAPI(conf)
        self.__queue = Queue.Queue()

    def singlePut(self, timestamp, value, tags):
        '''
        Put single data point into OpenTSDB.
        Returns feedback for a single put

        value: string, int, float, boolean
        tags: API.Tags
        timestamp: time in int (millisecond precision). Leaving it None will use the current system time.
            Note: Python built-in time.time() function returns a float in seconds. Using now() or getTimestamp(time) function is recommended
        '''
        if timestamp == None: timestamp = self.now()
        putData = PutData(timestamp, value, tags)
        return self.api.singlePut(putData)

    def multiplePut(self, valueTuples):
        '''
        Put multiple data points into OpenTSDB.
        Returns feedback for multiple put

        valueTuples: list<(timestamp, value, tags)>
        '''

        # TODO: Add data validation
        datas = []
        for tup in valueTuples:
            datas += [PutData(tup[0], tup[1], tup[2].copy())]
        return self.api.multiplePut(datas)

    def now(self):
        '''
        Returns the current timestamp
        '''
        return int(round(time.time() * 1000))

    def singleQuery(self, start, end, tags, aggregator = None):
        '''
        Returns the query result in JSON from given start time, end time, and tags

        start: start timestamp to query. Standard int in millisecond precision.
        end: end timestamp to query. Standard int in millisecond precision.
        tags: API.Tags
        '''
        query = QueryData(tags, aggregator)
        return self.api.singleQuery(start, end, query)

    def getTimestamp(self, time):
        '''
        Returns the standard timestamp with given time

        time: Python specific time in float
        '''
        return int(round(time * 1000))

    def toPythonTime(self, timestamp):
        return timestamp / 1000.0