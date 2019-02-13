import requests, base64, lyricsgenius, json
import re, sys, os, subprocess
from urllib.parse import urlencode, quote_plus
from collections import OrderedDict
from flask import Flask, render_template, send_from_directory, request, redirect, jsonify
from io import StringIO
from itertools import zip_longest
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape
from reader import Reader
from spotifyreader import get_client_id
from operator import itemgetter
from werkzeug.serving import run_simple

PORT = 8000

def pairwise(t):
    it = iter(t)
    l = zip_longest(it, it, fillvalue = None)
    return [(b, a) if b is not None else (a, b) for a, b in l]

if not os.path.exists('cache'):
    os.makedirs('cache')

debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == "--debug":
        debug = True

with open('spotify_secret.json', 'r') as f:
    data = json.load(f)

reader = Reader()
session = requests.Session()
client_id = data['second_id']
client_secret = data['second_secret']
access_token = data['genius_secret']
spotify_authorize = 'Basic ' + str(base64.b64encode((client_id + ':' + client_secret).encode('ascii')))[2:-1]
genius = lyricsgenius.Genius(access_token)
app = Flask(__name__, template_folder = 'templates')

@app.errorhandler(KeyError)
def page_not_found(err):
  return render_template('404.html'), 404

@app.route('/')
def main_page():
    return render_template('homepage.html', members = reader.people.keys(),
                           albums = pairwise(reader.albums[::-1]),
                           albumtitles = [album.title for album in reader.albums])

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

@app.route('/lyrics')
def lyrics():
    return render_template('lyrics.html')

@app.route('/lyrics/request')
def lyrics_request():
    song = request.args.get('song')
    artist = request.args.get('artist')
    id = request.args.get('id')
    filename = 'cache/%s.chc' % id
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            song = genius.search_song(song, artist)
            f.write(json.dumps(song.lyrics))
    return send_from_directory('cache', filename = id + ".chc")

@app.route('/lyrics/login')
def lyrics_login():
    redirect_uri = request.host_url + 'lyrics/callback'
    scope = 'user-read-currently-playing user-read-playback-state'
    querystr = urlencode(OrderedDict(
        response_type = 'code',
        client_id = client_id,
        scope = scope,
        show_dialog = 'true',
        redirect_uri = redirect_uri
    ), quote_via = quote_plus)
    return redirect('https://accounts.spotify.com/authorize?' + querystr)

@app.route('/lyrics/refresh_token')
def lyrics_refresh_token():
    refresh_token = request.args.get('token')
    result = session.post(url = 'https://accounts.spotify.com/api/token',
        data = {
          'grant_type': 'refresh_token',
          'refresh_token': refresh_token
        }, headers = {
        'Authorization' : spotify_authorize
        }).json()
    token = result['access_token']
    return json.dumps(token)

@app.route('/lyrics/callback')
def lyrics_callback():
    code = request.args.get('code')
    redirect_uri = request.host_url + 'lyrics/callback'
    result = session.post(url = 'https://accounts.spotify.com/api/token',
        data = {
          'code': code,
          'redirect_uri': redirect_uri,
          'grant_type': 'authorization_code'
        }, headers = {
        'Authorization' : spotify_authorize
        }).json()

    acc, refr = result['access_token'], result['refresh_token']
    tokens = urlencode(OrderedDict(access_token = acc, refresh_token = refr))
    return redirect(request.base_url.replace('/callback', '?') + tokens)

@app.route('/webhook', methods = ['POST'])
def webhook():
    payload = request.get_json()
    if payload.get('refs') == "/refs/heads/master":
        print("Trying to pull new changes from git...")
        try:
            cmd_output = subprocess.check_output(['git', 'pull', 'origin', 'master'])
            return jsonify({'msg': str(cmd_output)})
        except subprocess.CalledProcessError as error:
            print("Code deployment failed!\n%s" % str(error.output))
            return jsonify({'msg': str(error.output)})
    else:
        return jsonify({'msg': 'Not interested in %s' % str(payload.get(refs))})

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
    run_simple('0.0.0.0', PORT, app, use_reloader = True)
