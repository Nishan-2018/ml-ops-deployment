from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    # Check if index.html content is served (simple check)
    assert "text/html" in response.headers["content-type"]

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "model_loaded": True}

def test_predict_price():
    # Test with valid input
    payload = {
        "med_inc": 8.3252,
        "house_age": 41.0,
        "ave_rooms": 6.984127,
        "population": 322.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "price" in data
    assert isinstance(data["price"], float)
    assert data["price"] > 0

def test_predict_invalid_input():
    # Test with missing field
    payload = {
        "med_inc": 8.3252,
        "house_age": 41.0,
        "ave_rooms": 6.984127
        # Missing population
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Validation error
