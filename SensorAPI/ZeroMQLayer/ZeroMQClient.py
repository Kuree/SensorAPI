import sys
import zmq

import logging
import json

class Client(object):

    def __init__(self):
        self.REQUEST_TIMEOUT = 2500
        self.REQUEST_RETRIES = 3
        self.SERVER_ENDPOINT = ""
        self.__client = None
        self.context = None
        self.__poll = None
        

    def _connect(self):
        logging.info("Connecting to the server")
        self.context = zmq.Context(1)
        self.__client = self.context.socket(zmq.REQ)
        self.__client.connect(self.SERVER_ENDPOINT)
        self.__poll = zmq.Poller()
        self.__poll.register(self.__client, zmq.POLLIN)
        
        pass

    def _sendData(self, data):
        retry = self.REQUEST_RETRIES
        while retry >= 0:
            request = data
            logging.debug("Sending {0}".format(request))
            self.__client.send_json(request)
            expect_reply = True

            socks = dict(self.__poll.poll(self.REQUEST_TIMEOUT))
            if socks.get(self.__client) == zmq.POLLIN:
                reply = self.__client.recv()
                logging.debug("Received {0}".format(reply))
                return reply
            else:
                logging.error("No response from server, retrying again")
                # Socket is confused. Close and remove it
                self.__client.setsockopt(zmq.LINGER, 0)
                self.__client.close()
                self.__poll.unregister(self.__client)

                # retry
                retry -= 1

                # Create a new connection
                self.__client = self.context.socket(zmq.REQ)
                self.__client.connect(self.SERVER_ENDPOINT)
                self.__poll.register(self.__client)

    def _close(self):
        logging.debug("Closing client")
        self.__client.term()


            