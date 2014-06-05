import ConfigParser
import os.path
import random

class Configuration:

    def __init__(self):
        self.host = None
        self.port = None
        self.sensorID = None
        self.sensorType = None
        self.location = None
        if os.path.isfile("conf"):
            self.loadConfiguration()
        else:
            self.createConfiguration()
            self.saveConfiguration()

    def createConfiguration(self):
        self.host = "localhost"
        self.port = 4242
        self.sensorID = str(random.randint(1, 100000))
        self.sensorType = "Unknown"
        self.location = "Unknown"


    def saveConfiguration(self):
        config = ConfigParser.RawConfigParser()
        config.add_section("HostInformation")
        config.set("HostInformation", "host", self.host)
        config.set("HostInformation", "port", self.port)
        config.add_section("SensorInformation")
        config.set("SensorInformation", "sensorID", self.sensorID)
        config.set("SensorInformation", "sensorType", self.sensorType)
        config.set("SensorInformation", "location", self.location)
        with open('conf', 'wb') as configfile:
            config.write(configfile)

    def loadConfiguration(self):
        config = ConfigParser.RawConfigParser()
        config.read("conf")
        self.host = config.get("HostInformation", "host")
        self.port = config.getint("HostInformation", "port")
        self.sensorID = config.get("SensorInformation", "sensorID")
        self.sensorType = config.get("SensorInformation", "sensorType")
        self.location = config.get("SensorInformation", "location")

    def configExists():
        return os.path.isfile("conf")