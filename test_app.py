from app import app


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_data(as_text=True) == '{"status":"ok"}\n'
