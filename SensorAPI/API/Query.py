import re
import logging

class QueryAggregator(object):
    Sum = "sum"
    Min = "min"
    Max = "max"
    Average = "avg"
    StandardDeviation = "dev"

class QueryData(object):
    """Single query data"""
    def __init__(self, tags, aggregator, downSample):
        '''Initialize the query
        '''
        self.tags = tags
        self.downSample = downSample
        if aggregator == None:
            self.aggregator = QueryAggregator.Average
        else:
            self.aggregator  = aggregator
        self.logger = logging.getLogger("SensorAPI_API")

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("QueryData object created. metric: {0}, aggregator = {1}".format(self.tags.metric, self.aggregator))

    def toQueryData(self):
        result = {}
        result["metric"] = self.tags.metric
        result["tags"] = self.tags.toTagData()
        result["aggregator"] = self.aggregator
        if self.downSample != None:
            result["downsample"] = self.downSample.toDownSampleData()

        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("Raw QueryData created. metric: {0}, aggregator = {1}".format(self.tags.metric, self.aggregator))
        return result


class DownSample:
    def __inif__(self, downsampleRate, aggregator):
        self.aggregator = aggregator
        m = re.search("\d+[s,m]", downsampleRate, aggregator)
        if m:
            self.downsampleRate = downsampleRate
        else:
            self.downsampleRate = "1m"

    def toDownSampleData(self):
        return "{0}-{1}".format(self.downsampleRate, self.aggregator)