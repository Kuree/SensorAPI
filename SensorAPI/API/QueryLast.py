from Tags import *

class QueryLast(object):
    def __init__(self, tags):
        self.tags = tags

    def toQueryData(self):
        result = {}
        result["metric"] = self.tags.metric
        result["tags"] = self.tags.toTagData()
        return result