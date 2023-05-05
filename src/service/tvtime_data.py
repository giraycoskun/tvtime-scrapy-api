from fastapi import Depends
from typing import Annotated

from src.repository.redis_repository import RedisOMClient


class TVTimeDataService:
    def __init__(self, redis_client: Annotated[RedisOMClient, Depends()]):
        self.redis = redis_client

    def get_status(self, username):
        status = {
            "exists": self.redis.exists(username),
            "ttl": self.redis.get_ttl(username),
        }
        return status

    def get_all_data(self, username):
        return self.redis.get_tvtime_data(username)

    def get_watch_next(self, username):
        return self.redis.get_tvtime_watch_next(username)

    def get_not_watched_for_while(self, username):
        return self.redis.get_tvtime_not_watched_for_while(username)

    def get_not_started_yet(self, username):
        return self.redis.get_tvtime_not_started_yet(username)
