import requests, base64, lyricsgenius, json
import sys, os, re, subprocess
from urllib.parse import urlencode, quote_plus
from collections import OrderedDict
from flask import Flask, render_template, send_from_directory, request, redirect, jsonify, make_response
from itertools import zip_longest
from reader import Reader
from werkzeug.serving import run_simple
import passwordmanager as db

PORT = 8000

def pairwise(t):
    it = iter(t)
    l = zip_longest(it, it, fillvalue = None)
    return [(b, a) if b is not None else (a, b) for a, b in l]

if not os.path.exists('cache'):
    os.makedirs('cache')

fullchain = '/etc/letsencrypt/live/bigmusicjerk.com/fullchain.pem'
privkey   = '/etc/letsencrypt/live/bigmusicjerk.com/privkey.pem'
debug = not (os.path.exists(fullchain) and os.path.exists(privkey))

if len(sys.argv) > 1:
    if sys.argv[1] == "--debug":
        debug = True

with open('spotify_secret.json', 'r') as f:
    data = json.load(f)

reader = Reader(debug)
session = requests.Session()
client_id = data['second_id']
client_secret = data['second_secret']
genius_token = data['genius_secret']
spotify_authorize = 'Basic ' + str(base64.b64encode((client_id + ':' + client_secret).encode('ascii')))[2:-1]
genius = lyricsgenius.Genius(genius_token)
app = Flask(__name__, template_folder = 'templates')

if not debug:
    @app.before_request
    def before_request():
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)

@app.errorhandler(KeyError)
def page_not_found(err = None):
  return render_template('404.html'), 404

@app.route('/')
def main_page():
    print(request.cookies)
    resp = make_response(render_template(
        'homepage.html', members = reader.people.keys(),
        albums = pairwise(reader.albums[::-1]),
        albumtitles = [album.title for album in reader.albums]
    ))
    return resp

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

@app.route('/lyrics/')
def lyrics():
    return render_template('lyrics.html')

@app.route('/lyrics/request')
def lyrics_request():
    song = request.args.get('song')
    artist = request.args.get('artist')
    id = request.args.get('id')
    song = re.sub(r'\s?[-/] [^-/]*?[Rr]emaster(ed)?[^-/]*$', '', song)
    cache = request.args.get('cache', 'no')
    filename = 'cache/%s.json' % id
    if not os.path.isfile(filename):
        song = genius.search_song(song, artist)
        if song is None:
            lyrics = "\n\n\n\n\nNo lyrics found, you avant-garde bastard :/"
        else:
            lyrics = song.lyrics
        with open(filename, 'w') as f:
            f.write(json.dumps(lyrics))
    if cache == 'yes':
        print('Cached song %s for future use.' % (id + ".json"))
        return jsonify('Song has been cached.')
    print("Sending json file %s" % (id + ".json"))
    return send_from_directory('cache', filename = id + ".json")

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
    uid = request.cookies.get('uid')
    session_hash = request.cookies.get('session')
    redirect_uri = request.host_url + 'lyrics/callback'
    result = session.post(url = 'https://accounts.spotify.com/api/token',
        data = {
          'code': code,
          'redirect_uri': redirect_uri,
          'grant_type': 'authorization_code'
        }, headers = {
        'Authorization' : spotify_authorize
        }).json()

    access_token, refresh_token = result['access_token'], result['refresh_token']
    print("Testing...")
    if db.verify_login(uid, session_hash):
        print("Verified login!")
        db.set_tokens(uid, access_token, refresh_token)
        response = make_response(redirect('/lyrics/'))
        response.set_cookie('spotify_access', access_token)
        response.set_cookie('spotify_refresh', refresh_token)
        return response
    else:
        print("Login not verified!")
        tokens = urlencode(OrderedDict(access_token = access_token,
                                       refresh_token = refresh_token))
        return redirect('/lyrics/'.replace('/callback', '?') + tokens)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if db.check_password(username, password):
            uid, session_hash = db.login(username)
            print(uid, session_hash)
            response = make_response(redirect('/'))
            response.set_cookie('uid', str(uid))
            response.set_cookie('session', session_hash)
            return response
        else:
            error = "Invalid username/password!"
    resp = make_response(render_template('login.html', error = error))
    return resp

@app.route('/webhook', methods = ['POST'])
def webhook():
    payload = request.get_json()
    if payload.get('ref') == "refs/heads/master":
        print("Trying to pull new changes from git...")
        try:
            cmd_output = subprocess.check_output(['git', 'pull', 'origin', 'master'])
            return jsonify({'msg': str(cmd_output)})
        except subprocess.CalledProcessError as error:
            print("Code deployment failed!\n%s" % str(error.output))
            return jsonify({'msg': str(error.output)})
    else:
        return jsonify({'msg': 'Not interested in %s' % str(payload.get('ref'))})

@app.route('/.well-known/<path:path>')
def send_well_known(path):
    return send_from_directory('.well-known', path)

@app.route('/users/<username>/')
def user(username):
    name = username.lower()
    # FIXME: This line checks that user exists, should be done better
    if not reader.user_exists(username):
        return page_not_found()
    return render_template('person.html', name = name,
                           comparison_list = reader.get_likeness(name))

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    if debug:
        print('Running in debug mode! (http://localhost:8000/)')
        app.run('localhost', PORT, debug = True)
    else:
        print('Running in server mode! (DEBUG == off)')
        run_simple('0.0.0.0', PORT, app, use_reloader = True, ssl_context = (fullchain, privkey))
