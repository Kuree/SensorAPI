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
import collections
import csv
import io

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


class QueryHandler(tornado.web.RequestHandler):
    def post(self):
        result = self.mapReduce.queryResult(self.json_args)
        #result = self.client.sendData(self.json_args)
        self.write(json.dumps(result))

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def initialize(self, mapReduce):
        self.mapReduce = mapReduce

    def prepare(self):
        self.json_args = json_decode(self.request.body)


class OpenTSDBLookupHandler(tornado.web.RequestHandler):
    def post(self):
        self.write(json.dumps(self.client.lookup(self.json_args)))

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def initialize(self, client):
        self.client = client

    def prepare(self):
        self.json_args = json_decode(self.request.body)

class OpenTSDBToCSVHandler(tornado.web.RequestHandler):
    def post(self):
        self.write(self.openTSDB_to_CSV(self.json_args["openTSDB"], self.json_args["units"]))

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def prepare(self):
        self.json_args = json_decode(self.request.body)

    def openTSDB_to_CSV(self, openTSDB, units):

        if (len(openTSDB) != len(units)):
            return json.dumps({"error": "the inputs don't match up in number of time series"})
    
        # header included
        # separated by commas
        separator = ","

        header = ["Time Stamp"]
        all_data = {}
        for i in range(len(openTSDB)):
            header += [openTSDB[i]["name"] + ": " + units[i]]
            for point in openTSDB[i]["data"]:
                if (point["x"] not in all_data.keys()):
                    all_data[point["x"]] = []
                    for j in range(i):
                        all_data[point["x"]] += [""]
                all_data[point["x"]] += [point["y"]]
            for x_value in all_data.keys():
                if (len(all_data[x_value]) != i+1):
                    all_data[x_value] += [""]

        with io.BytesIO() as f:
           writer = csv.writer(f, delimiter=separator)
           writer.writerow(header)
           keys = all_data.keys()
           keys.sort()
           for key in keys:
               writer.writerow([time.asctime(time.gmtime(key))]+all_data[key])
           return f.getvalue()


class MySQLLookupHandler(tornado.web.RequestHandler):
    def post(self):
        self.write(self.getParameters())

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

        
    def getParameters(self):
        # Open database connection
        db = MySQLdb.connect("db.eg.bucknell.edu","sri","Hee1quai")

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        sql = "SELECT name FROM sri.sample_site"
        cursor.execute(sql)
        results = cursor.fetchall()

        sites = {}
        for row in results:
            sites[row[0]] = []

        sql = "SELECT name,units FROM sri.sample_parameter"
        cursor.execute(sql)
        param_results = cursor.fetchall()

        parameters = []
        for param in param_results:
            parameters += [{param[0]: param[1]}]

        for row in results:
            sites[row[0]] = parameters

        return sites



class MapReduce(object):
    '''
    MapReduce for OpenTSDB queries
    '''
    def __init__(self, client):
        self.client = client
        self.pool = multiprocessing.Pool(4)

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

        result =  self.pool.map(unPickledQuery, jobs)
        
        #result =  map(unPickledQuery, jobs)
        return result

_client = SensorClient()

import time

def unPickledQuery(job):
    print time.time()
    result = _client.sendData(job)
    if len(result) > 0:
        return json.loads(result)
    else:
        return ""


if __name__ == "__main__":
    
    mapReduce = MapReduce(_client)
    application = tornado.web.Application([
        ("/rickshaw", RickshawHandler, dict(mapReduce = mapReduce)),
        ("/opentsdb", OpenTSDBHandler, dict(mapReduce = mapReduce)),
        ("/opentsdblookup", OpenTSDBLookupHandler, dict(client = _client)),
        ("/query", QueryHandler, dict(mapReduce = mapReduce)),
        ("/mysqllookup", MySQLLookupHandler),
        ("/opentsdbtocsv", OpenTSDBToCSVHandler),
        ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()