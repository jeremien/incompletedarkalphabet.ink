from flask import Flask

app = Flask(__name__)

from incomplete import routes
from incomplete import cli
