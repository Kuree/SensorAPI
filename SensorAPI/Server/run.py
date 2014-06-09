import logging
from spyne.application import Application
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication

from Service import *
from util import *

if __name__=='__main__':
    # Python daemon boilerplate
    from wsgiref.simple_server import make_server
    logging.basicConfig(level=logging.DEBUG)

    application = Application([OpenTSDBService], 'bucknell.server.sensor',
          in_protocol=JsonDocument(),
          out_protocol=JsonDocument(),
      )

    wsgi_application = WsgiApplication(application)

    # More daemon boilerplate
    server = make_server(util.getIPAddress(), 8000, wsgi_application)

    logging.info("listening to http://{0}:8000".format(util.getIPAddress()))
    logging.info("wsdl is at: http://{0}:8000/?wsdl".format(util.getIPAddress()))

    server.serve_forever()