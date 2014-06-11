from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.primitive import String
import json
import requests
import Server.util
class OpenTSDBService(ServiceBase):

    @srpc(String, _returns=String)
    def put(data):
        jsonData = []
        for d in data:
            jsonData += [d]
        u = Server.util.util()
        ip = u.getServerIP()
        port = u.getServerPort()
        url = 'http://{0}:{1}/api/put?details'.format(ip, port)
        return OpenTSDBService._putRequest(url, jsonData)

    @srpc(String, _returns=String)
    def query(data):
        u = Server.util.util()
        ip = u.getServerIP()
        port = u.getServerPort()
        url = 'http://{0}:{1}/api/query'.format(ip, port)
        return OpenTSDBService._putRequest(url, data)

    @srpc(String, _returns=String)
    def querylast(data):
        # reserved for OpenTSDB 2.1
        u = Server.util.util()
        ip = u.getServerIP()
        port = u.getServerPort()
        url = 'http://{0}:{1}/api/query/last'.format(ip, port)
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

    def test(self):
        u = Server.util.util()
        ip = u.getServerIP()
        port = u.getServerPort()
        print ip, port
#