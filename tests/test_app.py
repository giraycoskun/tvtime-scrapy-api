import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.service import spider

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # The test runs here
    # Clean up code, if any

def test_read_main(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
