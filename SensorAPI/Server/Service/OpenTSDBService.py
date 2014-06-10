from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.primitive import String
import json
import requests

class OpenTSDBService(ServiceBase):

    @srpc(String, _returns=String)
    def put(data):
        jsonData = []
        for d in data:
            jsonData += [d]
        url = 'http://{0}:{1}/api/put?details'.format("134.82.132.98", 4242)
        return OpenTSDBService._putRequest(url, jsonData)

    @srpc(String, _returns=String)
    def query(data):
        url = 'http://{0}:{1}/api/query'.format("134.82.132.98", 4242)
        return OpenTSDBService._putRequest(url, data)

    @srpc(String, _returns=String)
    def querylast(data):
        url = 'http://{0}:{1}/api/query/last'.format("134.82.132.98", 4242)
        return OpenTSDBService._putRequest(url, data)

    @staticmethod
    def _putRequest(url, data):
        try:
            print "receive", data
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers)
            return r.text
        except Exception as e:
            return e.message
#