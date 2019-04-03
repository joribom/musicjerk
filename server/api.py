from flask import Blueprint, jsonify, make_response, redirect, request
from .reader import Reader

api_blueprint = Blueprint('api', __name__)
reader = Reader()

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@api_blueprint.route('/api/albums')
def albums():
    data = []
    albums = reader.albums
    for i in range(len(albums) - 1, 0, -2):
        mand = albums[i - 1]
        opt = albums[i]
        data.append((
            {'name': mand.title, 'artist': mand.artist, 'url' : mand.url, 'image' : mand.image_url},
            {'name': opt.title, 'artist': opt.artist, 'url' : opt.url, 'image' : opt.image_url}))
    mand = albums[0]
    data.append(({'name': mand.title, 'artist': mand.artist, 'url' : mand.url, 'image' : mand.image_url}, None))
    return jsonify(data)

@api_blueprint.route('/api/this-week')
def this_week():
    mand, opt = reader.albums[-2:]
    data = (
        {'name': mand.title, 'artist': mand.artist, 'url' : mand.url, 'image' : mand.image_url},
        {'name': opt.title, 'artist': opt.artist, 'url' : opt.url, 'image' : opt.image_url})
    return jsonify(data)


@api_blueprint.route('/api/members')
def members():
    return jsonify([name for name in reader.people.keys()])


@api_blueprint.route('/api/member/<name>/')
def member(name):
    return jsonify({'likeness': reader.get_likeness(name.lower()), 'albums': reader.get_ratings(name.lower())})

@api_blueprint.route('/api/albums/<albumname>/')
def album(albumname):
    album = reader.album_dict[albumname];
    data = {
        'name' : album.title,
        'artist' : album.artist,
        'summary' : album.summary,
        'genres' : album.genres,
        'styles' : album.styles,
        'spotify_id' : album.spotify_id,
        'image' : album.image_url
    }
    print(data)
    return jsonify(data)

@api_blueprint.route('/api/album-averages')
def album_averages():
    avgs = [{"title": album.title, "x": i, "y": album.rating, "url": album.url} for (i, album) in enumerate(reader.albums, 1) if album.rating != None]
    return jsonify(avgs)

@api_blueprint.route('/api/login', methods = ['POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
    response = jsonify(True)
    return response

@api_blueprint.route('/api/<path:path>', methods = ['POST', 'GET'])
def error_catch(path):
    raise InvalidUsage("This api page doesn't exist.", status_code=400)

@api_blueprint.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify({"error" : {"status" : error.status_code, "message" : error.message}})
    response.status_code = error.status_code
    return response
