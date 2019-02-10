import http.server, socketserver
from flask import Flask, render_template, send_from_directory
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

@app.route('/')
def main_page():
    return render_template('homepage.html', members = reader.people.keys(),
                           albums = list(zip(reader.albums[:-1][::-2], reader.albums[::-2])))

@app.route('/styles/<filename>')
def style(filename):
    return send_from_directory('styles', filename)

@app.route('/data/<filename>')
def data(filename):
    return send_from_directory('data', filename)

@app.route('/albums/')
def albums():
    return render_template('albums.html', albums = reader.albums)

@app.route('/albums/<albumname>/')
def album(albumname):
    album = reader.album_dict[albumname.lower()]
    return render_template('album.html', album = album)

@app.route('/users/<username>/')
def user(username):
    name = username.lower()
    # FIXME: This line checks that user exists, should be done better
    user = reader.people[name]
    return render_template('person.html', name = name,
                           comparison_list = reader.get_likeness(name))

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host = '0.0.0.0', port = PORT, debug=True)
