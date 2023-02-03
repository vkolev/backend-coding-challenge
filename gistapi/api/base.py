"""Base API Blueprint"""
from flask import Blueprint

api = Blueprint("base", __name__)


@api.get("/ping")
def ping():
    """Provide a static response to a simple GET request"""
    return "pong"
