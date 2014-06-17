import logging
logging.basicConfig(level=logging.DEBUG)
from spyne.application import Application
from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.primitive import Integer
from spyne.model.primitive import Unicode
from spyne.model.primitive import String
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication

class VisualizationService(ServiceBase):
    @srpc(String, _returns = Unicode)
    def query(name):
        data = []
        import time
        import random
        import json

        start = time.time() - 2 * 100000

        for i in range(10):
            dic = {}
            dic["x"] = start + i * 2000
            dic["y"] = i * 10
            data.append(dic)
        return json.dumps(data)

application = Application([VisualizationService],
    tns='spyne.examples.hello',
    in_protocol=HttpRpc(),
    out_protocol=JsonDocument()
)
if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('134.82.178.158', 8000, wsgi_app)
    server.serve_forever()