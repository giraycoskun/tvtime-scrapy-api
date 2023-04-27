import pytest
from fastapi.testclient import TestClient

from src.main import app

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # The test runs here
    # Clean up code, if any

def test_read_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_get_watch_next(test_app):
    response = test_app.get("/tvtime/watch-next")
    assert response.status_code == 201
