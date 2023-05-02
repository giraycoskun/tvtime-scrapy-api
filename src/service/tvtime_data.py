from fastapi import Depends
from typing import Annotated

from src.repository.redis_repository import RedisOMClient


class TVTimeDataService:
    def __init__(self, redis_client: Annotated[RedisOMClient, Depends()]):
        self.redis = redis_client

    def get_all_data(self, username):
        return self.redis.get_tvtime_data(username)
