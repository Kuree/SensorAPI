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

class RickshawHandler(tornado.web.RequestHandler):
    def post(self):
        #data = self.json_args
        data = json.loads(self.client.postQuery(self.json_args))
        result = []
        try:
            for dic in data:
                name = dic["metric"]
                for tagK, tagV in dic["tags"].iteritems():
                    name += ".{0}:{1}".format(tagK, tagV)
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

    def initialize(self, client):
        self.client = client

    def prepare(self):
        self.json_args = json_decode(self.request.body)

class OpenTSDBHandler(tornado.web.RequestHandler):
    def post(self):
        self.write(self.client.postQuery(self.json_args))

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def initialize(self, client):
        self.client = client

    def prepare(self):
        self.json_args = json_decode(self.request.body)



client = SensorClient()
application = tornado.web.Application([
    ("/rickshaw", RickshawHandler, dict(client=client)),
    ("/opentsdb", OpenTSDBHandler, dict(client=client)),
    ])
application.listen(8888)
tornado.ioloop.IOLoop.instance().start()