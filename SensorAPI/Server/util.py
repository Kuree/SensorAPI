import socket
import os.path
import json

class util:
    @staticmethod
    def getIPAddress():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    @staticmethod
    def getOpenTSDBServerIP():
        if os.path.isfile("server.json"):
            server = json.load(open("server.json", "r"))
            return server["OpenTSDBServerIP"]
        else:
            return "localhost"

    @staticmethod
    def getOpenTSDBServerPort():
        if os.path.isfile("server.json"):
            server = json.load(open("server.json", "r"))
            return server["OpenTSDBServerPort"]
        else:
            return 4242

    @staticmethod
    def getDataAPIPort():
        if os.path.isfile("server.json"):
            server = json.load(open("server.json", "r"))
            return server["DataAPIPort"]
        else:
            return 8000

    @staticmethod
    def getVisualServerPort():
        if os.path.isfile("server.json"):
            server = json.load(open("server.json", "r"))
            return server["VisualAPI"]
        else:
            return 8001