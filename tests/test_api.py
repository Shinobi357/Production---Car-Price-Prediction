import sys
import os
import pytest

sys.path.insert(0, os.path.abspath("src"))

from api import app

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
    assert "message" in response.get_json()

def test_predict_missing_json(client):
    response = client.post("/predict", json={})
    assert response.status_code == 400

def test_predict_missing_fields(client):
    response = client.post("/predict", json={"Year": 2020})
    assert response.status_code == 400
    assert "missing_fields" in response.get_json()
