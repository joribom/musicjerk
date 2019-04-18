import os
from flask import Flask
from werkzeug.serving import run_simple
from server.views import musicjerk_blueprint
from server.api import api_blueprint

PORT = 8000
fullchain = '/etc/letsencrypt/live/bigmusicjerk.com/fullchain.pem'
privkey = '/etc/letsencrypt/live/bigmusicjerk.com/privkey.pem'
debug = not (os.path.exists(fullchain) and os.path.exists(privkey))

app = Flask(
    __name__,
    static_folder='./templates/public',
    template_folder="./templates/static"
)
app.config.from_object('configurations.DevelopmentConfig')

# register the blueprints
app.register_blueprint(musicjerk_blueprint)
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = False
    if debug:
        print('Running in debug mode! (http://localhost:8000/)')
        app.run(
            'localhost',
            PORT,
            debug=True
        )
    else:
        print('Running in server mode! (DEBUG == off)')
        run_simple(
            '0.0.0.0',
            PORT,
            app,
            use_reloader=True,
            ssl_context=(fullchain, privkey)
        )
