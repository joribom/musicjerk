import SimpleHTTPServer
import SocketServer
from reader import Reader
import re

PORT = 8000

reader = Reader()

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            name = re.match('/(\w+)(.png)?', self.path)
            if name:
                reader.generate_fig(name.group(1).replace(".png", ""))
                self.path = '/' + name.group(1).replace(".png", "") + '.png'
        self.path = '/data' + self.path
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
