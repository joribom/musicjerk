import json
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


@api_blueprint.route('/api/validate', methods=['POST'])
def validate():
    jsondata = request.json.get('data', {})
    uid = jsondata.get('uid')
    session = jsondata.get('session')
    if uid is None or session is None:
        return jsonify({'authenticated': False})
    authenticated, username = dbauth.verify_login(uid, session)
    print(authenticated)
    print(username)
    data = {
        'authenticated': authenticated,
        'username': username
    }
    return jsonify(data)
