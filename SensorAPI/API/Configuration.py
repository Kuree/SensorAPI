import ConfigParser
import random
import os.path
import json
import logging

class Configuration(object):

    def __init__(self, filename = ""):
        self.logger = logging.getLogger("SensorAPI_API")
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("Starting to read configuration file")
        if len(filename) > 0:
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug("Using given filename: {0}".format(filename))
            self.loadConfiguration(filename)
            return
        elif os.path.isfile("client.json"):
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug("Using default client.json")
            self.loadConfiguration("client.json")
        else:
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug("Creating default client.json")
            self.__cfg = {}
            self.__cfg["host"] = "localhost"
            self.__cfg["port"] = "5555"
            self.__cfg["tags"] = {}
            self.saveConfiguration()

        self.logger.info("Configuration loaded. Queue host: {0}, port: {1}".format(self.__cfg["host"], self.__cfg["port"]))


    def saveConfiguration(self, filename = ""):
        if len(filename) == 0:
            filename = "client.json"    # create a master json in the main folder
        file = open(filename, "w")
        file.write(json.dump(self.__cfg))
        file.close()
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("Configuration saved at {0}".format(filename))
       
    def getQueueHost(self):
        return self.__cfg["host"]

    def getQueuePort(self):
        return int(self.__cfg["port"])

    def loadConfiguration(self, filename):  
        self.__cfg = json.load(open(filename, 'r'))
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("Configuration loaded from {0}".format(filename))

