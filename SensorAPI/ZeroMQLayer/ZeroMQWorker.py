from random import randint
import time
import zmq
import requests
import json

class ZeroMQWorker:
    def __init__(self):
        self.HEARTBEAT_LIVENESS = 3
        self.HEARTBEAT_INTERVAL = 1
        self.INTERVAL_INIT = 1
        self.INTERVAL_MAX = 32

        #  Paranoid Pirate Protocol constants
        self.PPP_READY = "\x01"      # Signals worker is ready
        self.PPP_HEARTBEAT = "\x02"  # Signals worker heartbeat


        self.worker = None
        self.context = None
        self.poller = None

        pass

    def connect(self):
        self.context = zmq.Context(1)
        self.worker = self.context.socket(zmq.DEALER)   # Dealer
        self.poller = zmq.Poller()

        identity = "%04X-%04X" % (randint(0, 0x10000), randint(0, 0x10000))
        self.worker.setsockopt(zmq.IDENTITY, identity)
        self.poller.register(self.worker, zmq.POLLIN)
        self.worker.connect("tcp://localhost:5556")
        self.worker.send(self.PPP_READY)


    def run(self):
        liveness = self.HEARTBEAT_LIVENESS
        interval = self.INTERVAL_INIT

        heartbeat_at = time.time() + self.HEARTBEAT_INTERVAL
        cycles = 0

        while True:
            socks = dict(self.poller.poll(self.HEARTBEAT_INTERVAL * 1000))

            # Handle worker activity on backend
            if socks.get(self.worker) == zmq.POLLIN:
                #  Get message
                #  - 3-part envelope + content -> request
                #  - 1-part HEARTBEAT -> heartbeat
                frames = self.worker.recv_multipart()
                if not frames:
                    break # Interrupted

                if len(frames) == 3:
                    print "I: Normal reply"

                    frames[2] = self.__postRequests(frames[2]).encode('ascii', 'ignore')

                    self.worker.send_multipart(frames)
                    liveness = self.HEARTBEAT_LIVENESS


                elif len(frames) == 1 and frames[0] == self.PPP_HEARTBEAT:
                    #print "I: Queue heartbeat"
                    liveness = self.HEARTBEAT_LIVENESS
                else:
                    print "E: Invalid message: %s" % frames
                interval = self.INTERVAL_INIT
            else:
                liveness -= 1
                if liveness == 0:
                    print "W: Heartbeat failure, can't reach queue"
                    print "W: Reconnecting in %0.2f..." % interval
                    time.sleep(interval)

                    if interval < self.INTERVAL_MAX:
                        interval *= 2
                    self.poller.unregister(worker)
                    self.worker.setsockopt(zmq.LINGER, 0)
                    self.worker.close()

                    self.connect()  # reconnect

                    liveness = self.HEARTBEAT_LIVENESS
            if time.time() > heartbeat_at:
                heartbeat_at = time.time() + self.HEARTBEAT_INTERVAL
                #print "I: Worker heartbeat"
                self.worker.send(self.PPP_HEARTBEAT)

    def __postRequests(self, jsData):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = json.loads(jsData)
        method = data["method"]
        requestData = data["data"]
        url = "http://134.82.132.98:4242/api/{0}".format(method)
        r = requests.post(url, data=json.dumps(requestData), headers=headers)
        return r.text


worker = ZeroMQWorker()
worker.connect()
worker.run()
