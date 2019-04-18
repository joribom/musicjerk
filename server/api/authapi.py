from flask import jsonify, request
from .dbutil import dbauth
from . import api_blueprint


@api_blueprint.route('/api/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if dbauth.check_password(username, password):
        response = {'auth': True}
        uid, session = dbauth.login(username)
        response['data'] = {
            'uid': uid,
            'session': session,
            'username': username
        }
        return jsonify(response)
    else:
        return jsonify({'auth': False})


@api_blueprint.route('/api/verify_login', methods=['POST'])
def verify_login():
    uid = request.form.get('uid')
    session = request.form.get('session')
    return jsonify(dbauth.verify_login(uid, session))
