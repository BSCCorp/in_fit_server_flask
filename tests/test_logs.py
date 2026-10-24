"""Tests for the logging endpoint."""


def test_log_appends_message(client, app):
    response = client.post(
        "/log",
        json={"message": "test message"},
    )

    assert response.status_code == 201
    assert app.config["LOG_FILE"].read_text() == "test message\n"


def test_log_appends_multiple_messages(client, app):
    client.post("/log", json={"message": "first"})
    client.post("/log", json={"message": "second"})

    assert app.config["LOG_FILE"].read_text() == "first\nsecond\n"


def test_log_accepts_form_data(client, app):
    response = client.post(
        "/log",
        data={"message": "form message"},
    )

    assert response.status_code == 201
    assert app.config["LOG_FILE"].read_text() == "form message\n"

def test_log_returns_400_when_file_cannot_be_written(client, app, tmp_path):
    # Create a regular file where the endpoint expects a directory.
    blocker = tmp_path / "blocker"
    blocker.write_text("x", encoding="utf-8")

    # Directory creation must fail because "blocker" is a file.
    app.config["LOG_FILE"] = blocker / "logs" / "output.log"

    response = client.post("/log", json={"message": "test"})

    assert response.status_code == 400

def test_log_missing_message_returns_400(client):
    response = client.post("/log", json={})

    assert response.status_code == 400
    assert response.is_json

def test_log_preserves_message_content(client, app):
    client.post("/log", json={"message": "line one\nline two"})

    assert app.config["LOG_FILE"].read_text() == "line one\nline two\n"


