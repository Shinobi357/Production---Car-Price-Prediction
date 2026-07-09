%%writefile tests/test_api.py
import pytest
from src.api import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "running"


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Car Price Prediction API" in response.data


def test_predict_missing_json(client):
    response = client.post("/predict")

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_predict_missing_fields(client):
    response = client.post(
        "/predict",
        json={
            "Year": 2018,
            "Brand": "Toyota"
        }
    )

    assert response.status_code == 400
    assert "missing_fields" in response.get_json()
