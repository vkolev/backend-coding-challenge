"""Global FLAKS error handlers"""

from flask import jsonify
from pydantic import ValidationError

from gistapi.schemas import ErrorResponse


def validation_error_handler(validation_error: ValidationError):
    """Global ValidationError handler"""
    return jsonify(
        ErrorResponse(
            status="failed",
            errors=[
                {"field": str(e.get("loc")[0]), "error": str(e.get("msg"))}
                for e in validation_error.errors()
            ],
        ).dict()
    )
