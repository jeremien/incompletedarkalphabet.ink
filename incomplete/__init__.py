import logging
from flask import Flask
from werkzeug.utils import find_modules, import_string

from incomplete import pages

def configure_logging():
    # register root logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('werkzeug').setLevel(logging.INFO)

def create_app():
    app = Flask(__name__)
    configure_logging()
    app.register_blueprint(pages.bp)
    return app
