import os
import subprocess
from flask import Flask, send_from_directory
from werkzeug.serving import run_simple

PORT = 8000

# Build react library
try:
    cmd_output = subprocess.check_output(
        'npm --prefix templates/static/ run build'.split(' ')
    )
except subprocess.CalledProcessError as error:
    print("Failed to build !\n%s" % str(error.output))
    exit(1)

fullchain = '/etc/letsencrypt/live/bigmusicjerk.com/fullchain.pem'
privkey   = '/etc/letsencrypt/live/bigmusicjerk.com/privkey.pem'
debug = not (os.path.exists(fullchain) and os.path.exists(privkey))

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
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    if debug:
        print('Running in debug mode! (http://localhost:8000/)')
        app.run('localhost', PORT, debug = True)
    else:
        print('Running in server mode! (DEBUG == off)')
        run_simple('0.0.0.0', PORT, app, use_reloader = True, ssl_context = (fullchain, privkey))
