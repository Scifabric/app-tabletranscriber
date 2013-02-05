import os
import pbclient

from flask import Flask
from app_tt import default_settings as settings


def create_app():
    app = Flask(__name__)
    configure_app(app)
    setup_pbclient(app)
    return app

def configure_app(app):
    app.config.from_object(settings)
    app.config.from_envvar('TT_SETTINGS', silent=True)
    # parent directory
    here = os.path.dirname(os.path.abspath( __file__ ))
    config_path = os.path.join(os.path.dirname(here), 'settings_local.py')
    if os.path.exists(config_path):
        app.config.from_pyfile(config_path)

def setup_pbclient(app):
    pbclient.set('endpoint', app.config['PYBOSSA_URL'])
    pbclient.set('api_key', app.config['API_KEY'])

app = create_app()
pbclient = pbclient
