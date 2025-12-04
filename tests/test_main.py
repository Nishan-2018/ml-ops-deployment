import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_read_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok', 'model_loaded': True}

def test_predict(client):
    response = client.post('/predict', json={'features': [5.1, 3.5, 1.4, 0.2]})
    assert response.status_code == 200
    assert 'class' in response.json()
