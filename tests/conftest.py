"""Shared pytest fixtures."""

import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "BASE_URL": "https://api.example.com",
            "RECEIVER_URL": "https://receiver.example.com",
            "VIDEO_DIR": tmp_path / "videos",
            "LOG_FILE": tmp_path / "logs" / "output.log",
        }
    )

    (tmp_path / "videos").mkdir()

    return app


@pytest.fixture
def client(app):
    return app.test_client()

