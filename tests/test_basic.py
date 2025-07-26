import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'


def test_shorten_url_invalid(client):
    response = client.post('/shorten', json={"url": "not-a-valid-url"})
    assert response.status_code == 400  # Assuming you return 400 for invalid URLs

def test_shorten_url(client):
    payload = { "url": "https://www.example.com/very/long/url" }
    response = client.post('/shorten', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'short_code' in data
    assert len(data['short_code']) > 0