import SimpleHTTPServer, SocketServer
from StringIO import StringIO
import re
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape
from reader import Reader

env = Environment(
    loader = FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

PORT = 8000

reader = Reader()

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def send_html_string(self, string):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(string)))
        self.end_headers()
        return StringIO(string)

    def send_head(self):
        if self.path.startswith('/data/'):
            template = env.get_template('person.html')
            name = self.path.replace('/data/', '').replace('.html', '').lower()
            if name in reader.people:
                body = template.render(name = name, comparison_list = reader.get_likeness(name))
                return self.send_html_string(body)
        return SimpleHTTPServer.SimpleHTTPRequestHandler.send_head(self)

    def do_GET(self):
        self.path = self.path.lower()
        if self.path.endswith('.png'):
            name = re.match('/(\w+).png', self.path)
            if name:
                name = name.group(1).lower().replace(".png", "")
                if name in reader.names:
                    reader.generate_fig(name)
        self.path = '/data' + self.path
        print "Get request for %s" % self.path
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyRequestHandler
SocketServer.TCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer(("", PORT), Handler)
try:
    print "serving at port", PORT
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    httpd.shutdown()
    print "Server closed!"
