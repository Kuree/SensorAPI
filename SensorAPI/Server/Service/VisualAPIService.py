from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.primitive import String
import json
import requests

class VisualizationService(ServiceBase):

    @srpc(String, _returns=String)
    def query(data):
        ip = Server.util.util.getIPAddress()
        port = Server.util.util.getDataAPIPort()
        url = 'tcp://{0}:{1}/query'.format(ip, port)
        rawData =  json.load(VisualizationService._putRequest(url, data))
        result = {}
        for data in rawData:
            dataPoint = data["metric"] + "."
            for k, v in data["tags"].iteritems():
                dataPoint += ".{0}.{1}".format(k, v)
            points = {}
            pointList = []
            dps = data["dps"]
            for timestamp, value in dps.iteritems():
                pointList.append({ "x" : long(timestamp), "y" : value})
            result[dataPoint] = pointList

        return json.dump(result)

        


    @staticmethod
    def _putRequest(url, data):
        try:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers)
            return r.text
        except Exception as e:
            return e.message