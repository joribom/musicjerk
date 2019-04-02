from flask import Blueprint, jsonify, make_response, redirect, request
from .reader import Reader

api_blueprint = Blueprint('api', __name__)
reader = Reader()

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

@api_blueprint.route('/api/login', methods = ['POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
    response = jsonify(True)
    return response
