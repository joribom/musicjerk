import http.server, socketserver
from flask import Flask, render_template
from io import StringIO
import re
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape
from reader import Reader

PORT = 8000

reader = Reader()
app = Flask(__name__, template_folder = 'templates')

@app.errorhandler(KeyError)
def page_not_found(err):
  return render_template('404.html'), 404

@app.route('/albums/<albumname>')
def index(albumname):
    album = reader.album_dict[albumname]
    return render_template('album.html', album = album)

if __name__ == '__main__':
    app.run(debug = True, port = PORT)

"""class MyRequestHandler(http.server.SimpleHTTPRequestHandler):

    def send_html_string(self, string):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(string)))
        self.end_headers()
        self.wfile.write(bytes(string, "utf8"))

    def send_head(self):
        if self.path.startswith('/data/'):
            name = self.path.replace('/data/', '').replace('.html', '').lower()
            name = name if not name.endswith('/') else name[:-1] # Remove trailing /
            if name in reader.people:
                template = env.get_template('person.html')
                body = template.render(name = name, comparison_list = reader.get_likeness(name))
                return self.send_html_string(body)
            elif name in ["", "index"]:
                template = env.get_template('homepage.html')
                body = template.render(members = reader.people.keys(), mandatory = reader.albums[-2],
                                       optional = reader.albums[-1])
                return self.send_html_string(body)
            elif name == "albums":
                template = env.get_template('albums.html')
                body = template.render(albums = [(album) for album in reader.albums])
                return self.send_html_string(body)
            elif name.replace('albums/', '') in reader.album_dict:
                album = reader.album_dict[name.replace('albums/', '')]
                template = env.get_template('album.html')
                body = template.render(album = album)
                return self.send_html_string(body)
        return http.server.SimpleHTTPRequestHandler.send_head(self)

    def do_GET(self):
        self.path = self.path.lower()
        if self.path.endswith('.png'):
            name = re.match('/([\w_]+).png', self.path)
            if name:
                name = name.group(1).lower().replace(".png", "")
                if name in reader.names:
                    reader.generate_fig(name)
                elif name == "average_ratings_over_time":
                    reader.generate_average_rating_over_time()
        if not self.path.endswith('.css'):
            self.path = '/data' + self.path
        print("Get request for %s" % self.path)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", PORT), MyRequestHandler)
try:
    print("serving at port", PORT)
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    httpd.shutdown()
    print("Server closed!")"""
