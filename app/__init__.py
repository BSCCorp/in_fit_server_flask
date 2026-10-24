"""Flask application factory."""

from flask import Flask, request

from app.config import Config
from app.errors import register_error_handlers
from app.routes.api import api_bp
from app.routes.health import health_bp
from app.routes.videos import videos_bp


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    register_error_handlers(app)

    app.register_blueprint(api_bp)
    app.register_blueprint(health_bp, url_prefix="/health")
    app.register_blueprint(videos_bp)

    @app.after_request
    def add_cors_headers(response):
        receiver_url = app.config.get("RECEIVER_URL", "")

        if receiver_url:
            response.headers["Access-Control-Allow-Origin"] = receiver_url

        if request.path.startswith("/videos/"):
            response.headers["Access-Control-Allow-Methods"] = "GET, HEAD, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = (
                "Origin, Content-Type, Accept, Range"
            )
            response.headers["Access-Control-Expose-Headers"] = (
                "Content-Length, Content-Range"
            )
        else:
            response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"

        return response

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            return "", 200

        return None

    return app
