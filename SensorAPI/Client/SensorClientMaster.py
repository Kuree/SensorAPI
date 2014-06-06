from API import *
from SensorClient import *
import os.path
import ConfigParser
from threading import Timer

class ClientMaster:
    def __init__ClientMaster(self):
        if not os.path.isfile("master.cfg"):
            self.createDefaultConfig()
        config = ConfigParser.RawConfigParser()
        config.read("master.cfg")
        self.confLocation = config.get("MasterConfiguration", "ConfigurationLocation")
        self.batchPeriod = config.get("NetworkConfiguration", "BatchPeriod")
        self.defaultHost = config.get("NetworkConfiguration", "DefaultHost")
        self.defaultPort = config.get("NetworkConfiguration", "DefaultPort")

        self.__clients = []
        self.__isBatching = False
        self.__timer = None

    def createDefaultConfig(self):
        config = ConfigParser.RawConfigParser()
        config.add_section("MasterConfiguration")
        config.set("MasterConfiguration", "ConfigurationLocation", "conf")
        config.add_section("NetworkConfiguration")
        config.set("NetworkConfiguration", "BatchPeriod", "60")
        config.set("NetworkConfiguration", "DefaultHost", "localhost")
        config.set("NetworkConfiguration", "DefaultPort", "4242")
        with open("master.cfg", 'wb') as configfile:
            config.write(configfile)
        return

    def addClient(self, client):
        self.__clients.append(client)

    def removeClient(self, client):
        self.__clients.remove(client)

    def batch(self, kvpList):
        if len(kvpList) < 0 or len(kvpList[0]) != 2:
            return 


    #def batchingForever(self):
    #    self.__isBatching = True
    #    self.batch()
    #    self.__timer = Timer(self.batchPeriod, self.batchingForever())
    #    self.__timer.start()

    def stopBatching(self):
        if self.__isBatching:
            self.__timer.cancel()