from flask import render_template, Blueprint

musicjerk_blueprint = Blueprint('musicjerk', __name__)

@musicjerk_blueprint.route('/', defaults={'path': ''})
@musicjerk_blueprint.route('/<path:path>')
def index(path):
    return render_template("index.html")
