def test_liveness_returns_ok(client):
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_readiness_returns_ok(client):
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_health_endpoints_return_json(client):
    for path in ("/health/live", "/health/ready"):
        response = client.get(path)

        assert response.is_json
