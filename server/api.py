from flask import Blueprint, jsonify, make_response, redirect, request
import urllib.parse
from . import dbreader

api_blueprint = Blueprint('api', __name__)

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
    data = dbreader.get_albums_basic()
    return jsonify(data)

@api_blueprint.route('/api/this-week')
def this_week():
    data = dbreader.get_this_weeks_albums()
    return jsonify(data)


@api_blueprint.route('/api/members')
def members():
    data = dbreader.get_members()
    return jsonify(data)


@api_blueprint.route('/api/member/<name>/')
def member(name):
    data = dbreader.get_member_info(name)
    return jsonify(data)

@api_blueprint.route('/api/albums/<albumname>/')
def album(albumname):
    albumname = urllib.parse.unquote(albumname)
    data = dbreader.get_album(albumname)
    return jsonify(data)

@api_blueprint.route('/api/album-averages')
def album_averages():
    avgs = dbreader.get_album_averages()
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
