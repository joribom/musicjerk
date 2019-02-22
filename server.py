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

def verify_cookie():
    uid = request.cookies.get('uid')
    session_hash = request.cookies.get('session')
    return db.verify_login(uid, session_hash)

def get_name():
    uid = request.cookies.get('uid')
    return db.get_name(uid);

def render_template_wrapper(*args, **kwargs):
    kwargs['name'] = get_name() if verify_cookie() else None
    return render_template(*args, **kwargs)

def set_cookies(response, username):
    uid, session_hash = db.login(username)
    response.set_cookie('uid', str(uid))
    response.set_cookie('session', session_hash)
    res = db.get_tokens(uid)
    for key, token in zip(('spotify_access', 'spotify_refresh'), res):
        if token is not None:
            response.set_cookie(key, token)

if not debug:
    @app.before_request
    def before_request():
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)

@app.errorhandler(404)
def page_not_found(err = None):
  return render_template_wrapper('404.html'), 404

@app.errorhandler(KeyError)
def _key_error(err = None):
    return page_not_found(err)

@app.route('/')
def main_page():
    print(request.cookies)
    resp = make_response(render_template_wrapper(
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
    return render_template_wrapper('albums.html', albums = reader.albums)

@app.route('/account/')
def account():
    if not verify_cookie():
        return page_not_found()
    return render_template_wrapper('account.html')

@app.route('/update_password', methods=['POST'])
def update_password():
    pass

@app.route('/albums/<albumname>/')
def album(albumname):
    album = reader.album_dict[albumname.lower()]
    return render_template_wrapper('album.html', album = album)

@app.route('/lyrics/')
def lyrics():
    return render_template_wrapper('lyrics.html')

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
    if db.verify_login(uid, session_hash):
        db.set_tokens(uid, access_token, refresh_token)
        response = make_response(redirect('/lyrics/'))
        response.set_cookie('spotify_access', access_token)
        response.set_cookie('spotify_refresh', refresh_token)
        return response
    else:
        tokens = urlencode(OrderedDict(access_token = access_token,
                                       refresh_token = refresh_token))
        return redirect('/lyrics?' + tokens)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if db.check_password(username, password):
            response = make_response(redirect('/'))
            set_cookies(response, username)
            return response
        else:
            error = "Invalid username/password!"
    elif verify_cookie():
        return page_not_found()
    resp = make_response(render_template_wrapper('login.html', error = error))
    return resp

@app.route('/logout')
def logout():
    if not verify_cookie():
        return page_not_found()
    response = make_response(redirect('/'))
    for key in request.cookies:
        response.set_cookie(key, '', expires = 0)
    return response

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
    return render_template_wrapper('person.html', name = name,
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
