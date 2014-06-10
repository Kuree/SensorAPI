class QueryAggregator(object):
    Sum = "sum"
    Min = "min"
    Max = "max"
    Average = "avg"
    StandardDeviation = "dev"

class QueryData(object):
    """Single query data"""
    def __init__(self, tags, aggregator):
        '''Initialize the query
        '''
        self.tags = tags
        if aggregator == None:
            self.aggregator = QueryAggregator.Average
        else:
            self.aggregator  = aggregator

    def toQueryData(self):
        result = {}
        result["metric"] = self.tags.metric
        result["tags"] = self.tags.toTagData()
        result["aggregator"] = self.aggregator
        return result


