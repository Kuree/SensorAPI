# int(round(time.time() * 1000))
class QueryData:
    """Single query data"""
    def __init__(self, location = "", sensorID = "", sensorType = "", aggregator = "sum",):
        '''Initialize the query
        '''
        self.location = location
        self.sensorID = sensorID
        self.sensorType = sensorType
        self.aggregator  = aggregator

    def toQueryData(self):
        result = {}
        result["metric"] = self.location
        result["tags"] = { "sensorID" : self.sensorID, "sensorType" : self.sensorType }
        result["aggregator"] = self.aggregator
        return result
