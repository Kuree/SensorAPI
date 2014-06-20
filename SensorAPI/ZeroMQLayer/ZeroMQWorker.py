from random import randint
import time
import zmq
import requests
import json
import logging
import ConfigParser
import os

class _WorkerConf(object):
    def __init__(self):
        self.__conf = ConfigParser.ConfigParser()
        if os.path.isfile("ZeroMQWorker.conf"):
            self.__conf.read("ZeroMQWorker.conf")
            logging.info("Using configuration file at ZeroMQWorker.conf")
        else:
            self.__conf.add_section("ZeroMQQueueServer")
            self.__conf.set("ZeroMQQueueServer", "ServerIP", "localhost")
            self.__conf.set("ZeroMQQueueServer", "ServerPort", 5556)
            self.__conf.add_section("Worker")
            self.__conf.set("Worker", "HeartBeatLiveness", 3)
            self.__conf.set("Worker", "HeartBeatInterval", 1.0)
            self.__conf.set("Worker", "IntervalInit", 1)
            self.__conf.set("Worker", "IntervalMax", 32)
            self.__conf.add_section("OpenTSDB")
            self.__conf.set("OpenTSDB", "ServerIP", "localhost")
            self.__conf.set("OpenTSDB", "ServerPort", 4242)
            logging.warn("Could not find ZeroMQWorker.conf, Use default setting now")

    def getQueueIP(self):
        return self.__conf.get("ZeroMQQueueServer", "ServerIP")

    def getQueuePort(self):
        return self.__conf.get("ZeroMQQueueServer", "ServerPort")

    def getWorkerHeartBeatLiveness(self):
        return self.__conf.getfloat("Worker", "HeartBeatLiveness")

    def getHeartBeatInterval(self):
        return self.__conf.getfloat("Worker", "HeartBeatInterval")

    def getWorkerIntervalInit(self):
        return self.__conf.getint("Worker", "IntervalInit")

    def getWorkerIntervalMax(self):
        return self.__conf.getint("Worker", "IntervalMax")

    def getOpenTSDBIP(self):
        return self.__conf.get("OpenTSDB", "ServerIP")

    def getOpenTSDBPort(self):
        return self.__conf.get("OpenTSDB", "ServerPort")

class ZeroMQWorker(object):
    def __init__(self):
        self.__conf = _WorkerConf()
        self.HEARTBEAT_LIVENESS = self.__conf.getWorkerHeartBeatLiveness()
        self.HEARTBEAT_INTERVAL = self.__conf.getHeartBeatInterval()
        self.INTERVAL_INIT = self.__conf.getWorkerIntervalInit()
        self.INTERVAL_MAX = self.__conf.getWorkerIntervalMax()

        self.QUEUE_SERVERIP = self.__conf.getQueueIP()
        self.QUEUE_SERVERPORT = self.__conf.getQueuePort()
        self.OPENTSDB_SERVERIP = self.__conf.getOpenTSDBIP()
        self.OPENTSDB_PORT = self.__conf.getOpenTSDBPort()

        #  Paranoid Pirate Protocol constants
        self.PPP_READY = "\x01"      # Signals worker is ready
        self.PPP_HEARTBEAT = "\x02"  # Signals worker heartbeat


        self.worker = None
        self.context = None
        self.poller = None

        self.s = requests.Session()
        # Get connection session
        self.s.get("http://{0}:{1}".format(self.OPENTSDB_SERVERIP, self.OPENTSDB_PORT))
        pass

    def connect(self):
        self.context = zmq.Context(1)
        self.worker = self.context.socket(zmq.DEALER)   # Dealer
        self.poller = zmq.Poller()

        identity = "%04X-%04X" % (randint(0, 0x10000), randint(0, 0x10000))
        self.worker.setsockopt(zmq.IDENTITY, identity)
        self.poller.register(self.worker, zmq.POLLIN)
        self.worker.connect("tcp://{0}:{1}".format(self.QUEUE_SERVERIP, self.QUEUE_SERVERPORT))
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
                    print "I: Queue heartbeat"
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
                    self.poller.unregister(self.worker)
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
        url = "http://{0}:{1}/api/{2}".format(self.OPENTSDB_SERVERIP, self.OPENTSDB_PORT, method)
        r = self.s.post(url, data=json.dumps(requestData), headers=headers)
        return r.text


worker = ZeroMQWorker()
worker.connect()
worker.run()
