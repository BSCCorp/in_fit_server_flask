"""Tests for the Clear Key endpoint."""


def test_key_returns_expected_structure(client, monkeypatch):
    from app.routes import api

    monkeypatch.setitem(
        api.KEYS,
        "1",
        {
            "k": "test-key",
            "kid": "test-key-id",
        },
    )

    response = client.get("/key/1")

    assert response.status_code == 200
    assert response.get_json() == {
        "keys": [
            {
                "kty": "oct",
                "k": "test-key",
                "kid": "test-key-id",
            }
        ],
        "type": "temporary",
    }


def test_unknown_key_returns_404(client):
    response = client.get("/key/unknown")

    assert response.status_code == 404

