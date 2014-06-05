import time
import Configuration

class PutData:
    """Single put data"""
    def __init__(self, timestamp = int(round(time.time())), value = None, conf = Configuration.Configuration()):
        self.timestamp = timestamp
        self.value = value
        self.conf = conf

    def toPutData(self):
        data = {}
        data["metric"] = self.conf.location
        data["timestamp"] = self.timestamp
        data["value"] = self.value
        data["tags"] = { "sensorID" : self.conf.sensorID, "sensorType" : self.conf.sensorType }
        return data