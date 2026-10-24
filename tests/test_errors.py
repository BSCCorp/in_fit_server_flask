def test_unknown_route_returns_404(client):
    response = client.get("/this-route-does-not-exist")

    assert response.status_code == 404
    assert response.is_json

    payload = response.get_json()

    assert payload["error"] == "Not Found"
    assert "message" in payload


def test_wrong_method_returns_405(client):
    response = client.post("/health/live")

    assert response.status_code == 405
    assert response.is_json
