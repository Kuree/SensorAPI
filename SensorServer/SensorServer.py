import API
import tornado.ioloop
import tornado.httpserver
import tornado.web
import inspect, os
from tornado.escape import json_decode
import json
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0,parentdir)
from SensorAPI.API.SensorClient import SensorClient
import multiprocessing

class RickshawHandler(tornado.web.RequestHandler):
    def post(self):
        #data = self.json_args
        data = self.mapReduce.queryResult(self.json_args)
        result = []
        try:
            if "error" in data:
                self.write(json.dumps(data))
                return
            for dic in data:
                name = dic["metric"]
                keyList = dic["tags"].keys()
                keyList.sort()
                for tagK in keyList:
                    name += ".{0}:{1}".format(tagK, dic["tags"][tagK])
                dps = []
                for timestamp, value in dic["dps"].iteritems():
                    point = {}
                    point["x"] = long(timestamp)
                    point["y"] = value
                    dps.append(point)
                dps = sorted(dps, key = lambda k: k["x"])
                result.append({name:dps})
            self.write(json.dumps(result))
        except:
            # error on the data
            self.write(data)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def initialize(self, mapReduce):
        self.mapReduce = mapReduce

    def prepare(self):
        self.json_args = json_decode(self.request.body)

class OpenTSDBHandler(tornado.web.RequestHandler):
    def post(self):
        self.write(json.dumps(self.mapReduce.queryResult(self.json_args)))

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def initialize(self, mapReduce):
        self.mapReduce = mapReduce

    def prepare(self):
        self.json_args = json_decode(self.request.body)


class QueryLastHandler(tornado.web.RequestHandler):
    def post(self):
        self.write(json.dumps(self.client.postQueryLast(self.json_args)))

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def initialize(self, client):
        self.client = client

    def prepare(self):
        self.json_args = json_decode(self.request.body)


class LookupHandler(tornado.web.RequestHandler):
    def post(self):
        self.write(json.dumps(self.client.lookup(self.json_args)))

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def initialize(self, client):
        self.client = client

    def prepare(self):
        self.json_args = json_decode(self.request.body)



class MapReduce(object):
    def __init__(self, client):
        self.client = client

    def _assignJobs(self, queryData):
        data = queryData
        if "queries" not in data:
            return {"error": "Incorrect query format"}
        if len(data["queries"]) == 1:
            return [data]
        else:
            start = data["start"]
            end = data["end"]
            result = []
            for query in data["queries"]:
                request = {}
                request["start"] = start
                request["end"] = end
                request["queries"] = [query]
                result.append(request)
            return result


    def queryResult(self, queryData):
        jobs = self._assignJobs(queryData)
        if  "error" in jobs:
            return jobs
        result = []
        #for job in jobs:
        #    result += json.loads(self.client.postQuery(job))

        pool = multiprocessing.Pool(4)
        result =  pool.map(unPickledQuery, jobs)
        return result[0]

_client = SensorClient()

import time
   
def unPickledQuery(job):
    print time.time()
    return json.loads(_client.postQuery(job))


if __name__ == "__main__":
    
    mapReduce = MapReduce(_client)
    application = tornado.web.Application([
        ("/rickshaw", RickshawHandler, dict(mapReduce = mapReduce)),
        ("/opentsdb", OpenTSDBHandler, dict(mapReduce = mapReduce)),
        ("/querylast", QueryLastHandler, dict(client = _client)),
        ("/lookup", QueryLastHandler, dict(client = _client)),
        ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()