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
    def getServerIP():
        if os.path.isfile("server.json"):
            server = json.load(open("server.json", "r"))
            return server["ServerIP"]
        else:
            return "localhost"

    @staticmethod
    def getServerPort():
        if os.path.isfile("server.json"):
            server = json.load(open("server.json", "r"))
            return server["ServerPort"]
        else:
            return "8000"