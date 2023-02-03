"""
Exposes a simple HTTP API to search a users Gists via a regular expression.

Github provides the Gist service as a pastebin analog for sharing code and
other develpment artifacts.  See http://gist.github.com for details.  This
module implements a Flask server exposing two endpoints: a simple ping
endpoint to verify the server is up and responding and a search endpoint
providing a search across all public Gists for a given Github account.
"""

from flask import Flask
from pydantic import ValidationError

from .api import base_route, gistapi_route
from .handlers import validation_error_handler


def create_app():
    """Application factory"""
    app = Flask(__name__)

    register_routes(app)
    register_handlers(app)
    return app


def register_routes(app: Flask):
    """Routes registration"""
    app.register_blueprint(base_route)
    app.register_blueprint(gistapi_route)


def register_handlers(app: Flask):
    """Register global handlers"""
    app.register_error_handler(ValidationError, validation_error_handler)
