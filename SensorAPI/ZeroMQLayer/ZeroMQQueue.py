from collections import OrderedDict
import time
import logging

import zmq



class Worker(object):
    def __init__(self, address):
        self.address = address
        self.HEARTBEAT_LIVENESS = 3     # 3..5 is reasonable
        self.HEARTBEAT_INTERVAL = 1.0   # Seconds

        self.expiry = time.time() + self.HEARTBEAT_INTERVAL * self.HEARTBEAT_LIVENESS
        

class WorkerQueue(object):
    def __init__(self):
        self.queue = OrderedDict()
        self.context = None
        self.frontend = None
        self.backend = None
        self.poll_both = None
        self.poll_workers = None
        self.heartbeat_at = 0.0

        self.HEARTBEAT_LIVENESS = 3     # 3..5 is reasonable
        self.HEARTBEAT_INTERVAL = 1.0   # Seconds

        #  Paranoid Pirate Protocol constants
        self.PPP_READY = "\x01"      # Signals worker is ready
        self.PPP_HEARTBEAT = "\x02"  # Signals worker heartbeat

    def connect(self):
        self.context = zmq.Context(1)
        self.frontend = self.context.socket(zmq.ROUTER)
        self.backend = self.context.socket(zmq.ROUTER)
        self.frontend.bind("tcp://*:5555") # For clients
        self.backend.bind("tcp://*:5556")  # For workers

        self.poll_workers = zmq.Poller()
        self.poll_workers.register(self.backend, zmq.POLLIN)

        self.poll_both = zmq.Poller()
        self.poll_both.register(self.frontend, zmq.POLLIN)
        self.poll_both.register(self.backend, zmq.POLLIN)
        self.heartbeat_at = time.time() + self.HEARTBEAT_INTERVAL


    def ready(self, worker):
        self.queue.pop(worker.address, None)
        self.queue[worker.address] = worker

    def run(self):
        heartbeat_at = time.time() + self.HEARTBEAT_INTERVAL

        while True:
            if len(self.queue) > 0:
                poller = self.poll_both
            else:
                poller = self.poll_workers
            socks = dict(poller.poll(self.HEARTBEAT_INTERVAL * 1000))

            # Handle worker activity on backend
            if socks.get(self.backend) == zmq.POLLIN:
                # Use worker address for LRU routing
                frames = self.backend.recv_multipart()
                if not frames:
                    break

                address = frames[0]
                self.ready(Worker(address))

                # Validate control message, or return reply to client
                msg = frames[1:]
                if len(msg) == 1:
                    if msg[0] not in (self.PPP_READY, self.PPP_HEARTBEAT):
                        logging.error("Invalid message from worker: %s" % msg)
                else:
                    self.frontend.send_multipart(msg)

                # Send heartbeats to idle workers if it's time
                if time.time() >= heartbeat_at:
                    for worker in self.queue:
                        msg = [worker, self.PPP_HEARTBEAT]
                        self.backend.send_multipart(msg)
                    heartbeat_at = time.time() + self.HEARTBEAT_INTERVAL
            if socks.get(self.frontend) == zmq.POLLIN:
                frames = self.frontend.recv_multipart()
                if not frames:
                    break

                frames.insert(0, self.next())
                self.backend.send_multipart(frames)

            self.purge()
            
    def purge(self):
        """Look for & kill expired workers."""
        t = time.time()
        expired = []
        for address,worker in self.queue.iteritems():
            if t > worker.expiry:  # Worker expired
                expired.append(address)
        for address in expired:
            logging.info("[WORKER]: Idle worker expired: %s" % address)
            self.queue.pop(address, None)

    def next(self):
        address, worker = self.queue.popitem(False)
        return address

queue = WorkerQueue()
queue.connect()
queue.run()