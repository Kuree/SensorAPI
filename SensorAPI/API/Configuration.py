import ConfigParser
import random
import os.path
import json

class Configuration(object):

    def __init__(self, filename = ""):
        if len(filename) > 0:
            self.loadConfiguration(filename)
            return
        elif os.path.isfile("master.json"):
            self.loadConfiguration("master.json")
        else:
            self.__cfg = {}
            self.__cfg["batchEnabled"] = False
            self.__cfg["host"] = "localhost"
            self.__cfg["port"] = "4242"
            self.__cfg["tags"] = {}


    def saveConfiguration(self, filename = ""):
        if len(filename) == 0:
            filename = "master.json"    # create a master json in the main folder
        file = open(filename, "w")
        file.write(json.dump(self.__cfg))
        file.close()
       
    def getHost(self):
        return self.__cfg["host"]

    def getPort(self):
        return int(self.__cfg["port"])

    def loadConfiguration(self, filename):  
        self.__cfg = json.load(open(filename, 'r'))

    def addTag(self, tagName):
        self.__cfg["tags"][tagName] = ""

    def updateTag(self, tagName, value):
        self.__cfg["tags"][tagName] = value

    def removeTag(self, tagName):
        if self.__cfg.has_key(tagName):
            self.__cfg["tags"].pop(tagName)
    def hasTag(self, tagName):
        return tagName in self.__cfg["tags"]

