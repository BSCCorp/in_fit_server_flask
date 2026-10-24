from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        response = jsonify(
            {
                "error": error.name,
                "message": error.description,
            }
        )

        response.status_code = error.code or 500

        return response

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        app.logger.exception("Unhandled application exception")

        return jsonify(
            {
                "error": "Internal Server Error",
                "message": "An unexpected error occurred.",
            }
        ), 500
