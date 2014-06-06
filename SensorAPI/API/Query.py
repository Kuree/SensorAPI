# int(round(time.time() * 1000))
class QueryData:
    """Single query data"""
    def __init__(self, tags, aggregator = "sum",):
        '''Initialize the query
        '''
        self.tags = tags
        self.aggregator  = aggregator

    def toQueryData(self):
        result = {}
        result["metric"] = self.tags.metric
        result["tags"] = self.tags.toTagData()
        result["aggregator"] = self.aggregator
        return result
