from API import *
from multiprocessing import Process, Queue
import time
class SensorClient:
    #def __init__(self, location = "unknown", sensorID = "unknown", sensorType = "unknown", master = None, filename = ""):
    #    if master == None:
    #        self.config = Configuration.Configuration(sensorID = sensorID,
    #                                              sensorType = sensorType, location = location)
    #    else:
    #        self.config = Configuration.Configuration(host = master.defaultHost, port= master.defaultPort,
    #                                                  sensorID = sensorID, sensorType = sensorType, location = location, filename = filename)
    #    self.__buff = Queue()

    #def pushToBuff(self, value):
    #    p = Process(target = self.__pushToBuff, args=(value,))
    #    p.start()
    #    p.join()

    #def __pushToBuff(self, value):
    #     self.__buff.put(SensorAPI.now(), value)

    #def batch(self):
    #    p = Process(target=self.__batch)
    #    p.start()
    #    p.join()

    #def __batch(self):
    #    pass
    def __init__(self, conf):
        self.conf = conf
        self.api = SensorAPI(conf)

    def singlePut(self, timestamp, value, tags):
        return self.api.singlePut(timestamp, value, tags)

    def multiplePut(self, valueTuples, tags):
        datas = []
        for tup in valueTuples:
            datas += [PutData(tup[0], tup[1], tags)]
        return self.api.multiplePut(datas)

    def now(self):
        return int(round(time.time() * 1000 ))

    def singleQuery(self, start, end, tags):
        return self.api.singleQuery(start, end, tags)

    
