import SimpleHTTPServer
import SocketServer
from reader import Reader
import re
from datetime import datetime, timedelta

PORT = 8000

reader = Reader()

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            name = re.match('/(\w+)(.png)?', self.path)
            if name:
                if datetime.now() - reader.latest_update > timedelta(minutes = 1):
                    reader.readValues()
                name = name.group(1).lower().replace(".png", "")
                if name in reader.names:
                    reader.generate_fig(name)
                    self.path = '/' + name + '.png'
        self.path = '/data' + self.path
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)
try:
    print "serving at port", PORT
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    httpd.server_close()
    print "Server closed!"

