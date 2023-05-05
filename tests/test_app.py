import pytest
from fastapi.testclient import TestClient
from os.path import exists
import redis
from pydantic import BaseModel
from typing import Optional
import logging

from src.main import app, write_openapi_spec
import src.repository.redis_repository


@pytest.fixture(scope="function")
def test_redis_mock():
    class RedisMock:
        def __init__(self, url="") -> None:
            pass

        def from_url(self, url="", decode_responses=True):
            return self

        def exists(self, key):
            return True

        def ttl(self, key):
            return 86364

    return RedisMock


@pytest.fixture(scope="function")
def test_redis_model_mock():
    class TVTimeDataModelMock(BaseModel):
        username: str
        user_id: Optional[str]
        to_watch: Optional[dict]
        upcoming: Optional[dict]
        profile: Optional[dict]

    class RedisModelMock:
        def get(self):
            data = {
                "username": "test_user",
                "user_id": "test_id",
                "to_watch": {
                    "Watch next": {
                        "Game of Thrones": {"episode": "S02E03", "is_new": True},
                        "Rick and Morty": {"episode": "S03E02", "is_new": False},
                    }
                },
                "upcoming": {},
                "profile": {},
            }
            return TVTimeDataModelMock(**data)

        class Meta:
            def database(self):
                pass

    return RedisModelMock


@pytest.fixture(scope="function")
def test_app(monkeypatch, test_redis_mock, test_redis_model_mock):
    monkeypatch.setattr(redis, "Redis", test_redis_mock)
    monkeypatch.setattr(
        src.repository.redis_repository, "get_redis_connection", test_redis_mock
    )
    monkeypatch.setattr(
        src.repository.redis_repository, "TVTimeDataModel", test_redis_model_mock
    )
    client = TestClient(app)
    yield client  # The test runs here
    # Clean up code, if any


def test_read_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_api_spec():
    write_openapi_spec(app)
    assert exists("./docs/assets/openapi.json")


def test_get_status(test_app):
    response = test_app.get("/status", params={"username": "test_user"})
    assert response.status_code == 200
    assert response.json() == {"exists": True, "ttl": 86364}


def test_get_all_data(test_app):
    response = test_app.get("/all-data", params={"username": "test_user"})
    assert response.status_code == 200
    assert response.json() == {
        "username": "test_user",
        "user_id": "test_id",
        "to_watch": {
            "Watch next": {
                "Game of Thrones": {"episode": "S02E03", "is_new": True},
                "Rick and Morty": {"episode": "S03E02", "is_new": False},
            }
        },
        "upcoming": {},
        "profile": {},
    }


def test_get_watch_next(test_app):
    response = test_app.get("/watch-next", params={"username": "test_user"})
    assert response.status_code == 200
    logging.debug(response.json())
    assert response.json() == {
        "Game of Thrones": {"episode": "S02E03", "is_new": True},
        "Rick and Morty": {"episode": "S03E02", "is_new": False},
    }


def test_get_not_watched_for_while(test_app):
    response = test_app.get("/not-watched-for-while", params={"username": "test_user"})
    assert response.status_code == 200
    assert response.json() == {}


def test_get_not_started_yet(test_app):
    response = test_app.get("/not-started-yet", params={"username": "test_user"})
    assert response.status_code == 200
    assert response.json() == {}
