"""TVTime Data Service

Returns:
    TVTimeDataService: Service to handle tvtime data
"""
from typing import Annotated

from fastapi import Depends, HTTPException

from src.service.security import get_current_active_user
from src.repository.redis_repository import RedisOMClient
from src.models.db import User


class TVTimeDataService:
    def __init__(
        self,
        tvtime_username: str,
        current_user: Annotated[User, Depends(get_current_active_user)],
        redis_client: Annotated[RedisOMClient, Depends()],
    ):
        self.redis = redis_client
        self.user = current_user
        self.tvtime_username = tvtime_username
        if not self.redis.check_tvtime_account_of_user(current_user.username, tvtime_username):
            raise HTTPException(status_code=404, detail="Scraped Data Not Found")

    def get_status(self):
        status = {
            "exists": self.redis.exists(self.tvtime_username),
            "ttl": self.redis.get_ttl(self.tvtime_username),
        }
        return status

    def get_all_data(self):
        return self.redis.get_tvtime_data(self.tvtime_username)

    def get_watch_next(self):
        return self.redis.get_tvtime_watch_next(self.tvtime_username)

    def get_not_watched_for_while(self):
        return self.redis.get_tvtime_not_watched_for_while(self.tvtime_username)

    def get_not_started_yet(self):
        return self.redis.get_tvtime_not_started_yet(self.tvtime_username)
