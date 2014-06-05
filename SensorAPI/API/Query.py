# int(round(time.time() * 1000)
class Query(object):
    """QueryData"""

    def __init__(self, start, end, location, sensorID):
        pass
    def __init__(self, location = "", sensorID = "", sensorType = "", aggregator = "",):
        self.location = location
        self.sensorID = sensorID
        self.sensorID = sensorType
        self.aggregator  = aggregator

    def toQueryData(self):
        result = {}
        result["metric"] = self.location
        result["tags"] = {"sensorID":self.sensorID, "sensorType":self.
        return result
