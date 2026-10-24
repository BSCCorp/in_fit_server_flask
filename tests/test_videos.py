"""Tests for video file serving."""


def test_video_is_served(client, app):
    video_path = app.config["VIDEO_DIR"] / "sample.mp4"
    video_path.write_bytes(b"sample video content")

    response = client.get("/videos/sample.mp4")

    assert response.status_code == 200
    assert response.data == b"sample video content"


def test_video_supports_range_requests(client, app):
    video_path = app.config["VIDEO_DIR"] / "sample.mp4"
    video_path.write_bytes(b"0123456789")

    response = client.get(
        "/videos/sample.mp4",
        headers={"Range": "bytes=0-3"},
    )

    assert response.status_code == 206
    assert response.data == b"0123"
    assert response.headers["Content-Range"] == "bytes 0-3/10"


def test_missing_video_returns_404(client):
    response = client.get("/videos/missing.mp4")

    assert response.status_code == 404


def test_video_is_served_from_nested_directory(client, app):
    video_path = (
        app.config["VIDEO_DIR"]
        / "jennifer-kries"
        / "the-method-pilates"
        / "target-specifics"
        / "00-introduction"
        / "stream.mpd"
    )
    video_path.parent.mkdir(parents=True, exist_ok=True)
    video_path.write_text(
        '<?xml version="1.0"?><MPD></MPD>',
        encoding="utf-8",
    )

    response = client.get(
        "/videos/jennifer-kries/the-method-pilates/"
        "target-specifics/00-introduction/stream.mpd"
    )

    assert response.status_code == 200
    assert b"<MPD>" in response.data
