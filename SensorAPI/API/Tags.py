from Configuration import *

class Tags:
    def __init__(self, conf, metric):
        self.__config = conf
        self.__tags = {}
        self.metric = metric

    def addTag(self, tagName, tagValue):
        if tagName not in self.__tags:
            self.__tags[tagName] = tagValue

    def toTagData(self):
        return self.__tags

    def getTags(self):
        return self.__tags.keys()
    
    def clearTags(self):
        self.__tags.clear()

    def updateTags(self, tagName, tagValue):
        if tagName in self.__tags:
            self.__tags[tagName] = tagValue

    def copy(self):
        new = Tags(self.__config, self.metric)
        new.__tags = self.__tags.copy()
        return new


    def __repr__(self):
        result = ""
        for k in self.__tags:
            result += "key: {0} value: {1}, ".format(k, self.__tags[k])
        return result[0:-2]
