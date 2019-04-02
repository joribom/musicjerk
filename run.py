from flask import Flask, send_from_directory

app = Flask(__name__,
    static_folder = './templates/public',
    template_folder="./templates/static")
app.config.from_object('configurations.DevelopmentConfig')

from server.views import musicjerk_blueprint
from server.api import api_blueprint

# register the blueprints
app.register_blueprint(musicjerk_blueprint)
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    app.run()
