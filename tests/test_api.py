import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_normal(client):
    response = client.post("/predict", json={"features": [0.1, -0.2, 0.3, 0.0]})
    assert response.status_code == 200
    body = response.json()
    assert "score" in body
    assert "is_anomaly" in body
    assert isinstance(body["score"], float)
    assert isinstance(body["is_anomaly"], bool)


def test_predict_wrong_features(client):
    response = client.post("/predict", json={"features": [1.0, 2.0]})
    assert response.status_code == 422


def test_metrics(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "predict_requests_total" in response.text
