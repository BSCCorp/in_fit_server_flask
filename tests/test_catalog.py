"""Tests for the video catalogue endpoint."""


def test_catalog_returns_six_videos(client):
    response = client.get("/")

    assert response.status_code == 200

    videos = response.get_json()

    assert isinstance(videos, list)
    assert len(videos) == 6
    assert [video["id"] for video in videos] == [
        "1", "2", "3", "4", "5", "6"
    ]


def test_catalog_preserves_response_fields(client):
    response = client.get("/")

    introduction = response.get_json()[0]

    assert introduction == {
        "id": "1",
        "title": "Introduction",
        "description": (
            "The Method's concept of integrated fitness allows you "
            "to learn and perform movements and exercises from four "
            "of the world's most proven physical conditioning "
            "philosophies: yoga, martial arts, classical dance, "
            "and the work of Joseph Pilates."
        ),
        "influencer": "Jennifer Kries",
        "thumbnail": (
            "https://api.example.com/videos/jennifer-kries/"
            "the-method-pilates/target-specifics/00-introduction/"
            "images/00-intro.jpg"
        ),
        "source": (
            "https://api.example.com/videos/jennifer-kries/"
            "the-method-pilates/target-specifics/00-introduction/"
            "stream.mpd"
        ),
        "contentType": "application/dash+xml",
        "aspectRatio": "4/3",
        "length": "1m",
        "category": "Pilates",
    }


def test_catalog_uses_configured_base_url(client):
    response = client.get("/")

    videos = response.get_json()

    assert all(
        video["source"].startswith("https://api.example.com/videos/")
        for video in videos
    )

