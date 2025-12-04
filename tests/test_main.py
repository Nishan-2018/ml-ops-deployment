from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_read_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok', 'model_loaded': True}

def test_predict():
    response = client.post('/predict', json={'features': [5.1, 3.5, 1.4, 0.2]})
    assert response.status_code == 200
    assert 'class' in response.json()
