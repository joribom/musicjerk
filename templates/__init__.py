from flask import Flask

app = Flask(__name__,
    static_folder = './public',
    template_folder="./static")

from templates.musicjerk.views import musicjerk_blueprint
from templates.musicjerk.api import api_blueprint

# register the blueprints
app.register_blueprint(musicjerk_blueprint)
app.register_blueprint(api_blueprint)
