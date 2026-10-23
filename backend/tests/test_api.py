from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_results_endpoint():
    response = client.get("/experiment/results")
    payload = response.json()

    assert response.status_code == 200
    assert payload["primary_metric"] == "conversion_rate"
    assert "sample_ratio_mismatch" in payload
