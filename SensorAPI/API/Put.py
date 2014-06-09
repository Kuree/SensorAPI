import time
import Configuration

class PutData(object):
    """Single put data"""
    def __init__(self, timestamp, value, tags):
        self.timestamp = timestamp
        # every value is converted to string
        self.value = value
        self.tags = tags.copy()
        self.metric = tags.metric

    def toPutData(self):
        data = {}
        data["metric"] = self.metric
        data["timestamp"] = self.timestamp
        data["value"] = self.value
        data["tags"] = self.tags.toTagData()
        return data