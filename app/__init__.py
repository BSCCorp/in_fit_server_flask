from flask import Flask

from app.config import Config
from app.errors import register_error_handlers
from app.routes import register_routes


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)

    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    register_routes(app)
    register_error_handlers(app)

    return app
