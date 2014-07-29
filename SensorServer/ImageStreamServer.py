import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.websocket
import base64
import json
import time
class ImageStream(tornado.websocket.WebSocketHandler):
    def open(self):
        print("connection opened")

    def on_message(self, message):
        request = json.loads(message)
        print request
        start = int(request["start"])
        end = int(request["end"])
        frequency = int(request["end"])
        
        images = [open("img.jpg", "rb").read()]
        imageBase64 = map(base64.b64encode, images) * 40

        for image in imageBase64:
            #data = base64.b64encode(image)
            self.write_message(image)
            time.sleep(1.0 / frequency)

class ImageHandler(tornado.web.RequestHandler):
    def post(self):
        self.render("test.html")

        #return super(ImageStream, self).on_message(message)

if __name__ == "__main__":
    
    application = tornado.web.Application([
        ("/image", ImageStream),])
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()