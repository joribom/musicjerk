from flask import Blueprint, jsonify, request
import subprocess
import urllib.parse
from .dbutil import dbreader
from . import api_blueprint

# api_blueprint = Blueprint('api', __name__)


def rebuild_react():
    # Install react dependencies, in case a new one is added
    try:
        cmd_output = subprocess.check_output(
            'npm --prefix templates/static/ install'.split(' ')
        )
        return cmd_output
    except subprocess.CalledProcessError as error:
        return("Failed to install deps!\n%s" % str(error.output))
    # Build react library
    try:
        cmd_output = subprocess.check_output(
            'npm --prefix templates/static/ run build'.split(' ')
        )
        return cmd_output
    except subprocess.CalledProcessError as error:
        return("Failed to build!\n%s" % str(error.output))


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


@api_blueprint.route('/api/login', methods=['POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
    response = jsonify(True)
    return response


@api_blueprint.route('/api/<path:path>', methods=['POST', 'GET'])
def error_catch(path):
    raise InvalidUsage("This api page doesn't exist.", status_code=400)


@api_blueprint.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_json()
    if payload.get('ref') == "refs/heads/master":
        print("Trying to pull new changes from git...")
        try:
            cmd_output = subprocess.check_output(
                ['git', 'pull', 'origin', 'master']
            )
            build_output = rebuild_react()
            return jsonify({'msg': str(cmd_output) + '\n' + build_output})
        except subprocess.CalledProcessError as error:
            print("Code deployment failed!\n%s" % str(error.output))
            return jsonify({'msg': str(error.output)})
    else:
        return jsonify(
            {'msg': 'Not interested in %s' % str(payload.get('ref'))}
        )


@api_blueprint.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(
        {"error": {"status": error.status_code, "message": error.message}}
    )
    response.status_code = error.status_code
    return response


# Rebuild react on initial import of file
rebuild_react()
