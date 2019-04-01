from flask import Blueprint, jsonify, make_response, redirect, request

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/albums')
def albums():
    return jsonify([{'name': 'Jedi Mind Tricks...', 'artist': 'Army Of The Pharaohs', 'url': '/albums/jedi_mind_tricks_presents_the_best_of_army_of_the_pharaohs_(disc_1)-army_of_the_pharaohs/', 'image': 'https://i.scdn.co/image/68f1d1295e415a273f3967be8e8e7ff1fa4c3037'},
                    {'name': 'Collection', 'artist': 'Misfits', 'url': '/albums/collection-misfits/', 'image': 'https://i.scdn.co/image/40f4551b6bb0fe6375fffb26d61028ff32a03012'},
                    {'name': 'Plastic Whatever', 'artist': 'Desired', 'url': '/albums/plastic_whatever-desired/', 'image': 'https://i.scdn.co/image/c06135b561085ecb53ffa8ab99e9713a5357cf73'},
                    {'name': 'Air', 'artist': 'Moon Safari', 'url': '/albums/moon_safari-air/', 'image': 'https://i.scdn.co/image/d4867dab43434e657a94f046bfa7ff304e2a4c8b'}])

@api_blueprint.route('/api/login', methods = ['POST'])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
    response = jsonify(True)
    return response
