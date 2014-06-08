from Configuration import *

class Tags:
    def __init__(self, conf, metric):
        self.__config = conf
        self.__tags = {}
        self.metric = metric

    def addTag(self, tagName, tagValue):
        if self.__config.hasTag(tagName) and tagName not in self.__tags:
            self.__tags[tagName] = tagValue

    def toTagData(self):
        return self.__tags

    def getTags(self):
        return self.__tags.keys()
    
    def clearTags(self):
        self.__tags.clear()

    def copy(self):
        new = Tags(self.__config, self.metric)
        new.__tags = self.__tags.copy()
        return new
