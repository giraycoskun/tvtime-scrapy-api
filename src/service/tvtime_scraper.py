"""TVTime Scraper Service

Returns:
    TVTimeScraperService: Service to handle scraper tasks
"""
from typing import Annotated

from celery.result import AsyncResult
from fastapi import Depends
from loguru import logger

from src.service.security import get_current_active_user
from src.repository.celery_repository import celery, scrape_task
from src.repository.redis_repository import RedisOMClient
from src.repository.postgre_repository import PostgreSQLClient, get_db
from src.repository.request_repositoy import TVTimeClient, get_tvtime_client
from src.models.db import User
from src.models.api import TVTimeUser
from src.models.exceptions import TVTimeLoginException

class TVTimeScraperService:
    """Service to Scrape TVTime"""

    def __init__(
        self,
        current_user: Annotated[User, Depends(get_current_active_user)],
        redis_client: Annotated[RedisOMClient, Depends()],
        tvtime_client: Annotated[TVTimeClient, Depends(get_tvtime_client)],
    ):
        self.user = current_user
        self.redis = redis_client
        self.tvtime = tvtime_client

    def scrape(self) -> str:
        """Start scrape task by checking if the user tvtime account is already in the database

        Args:
            user (TVTimeUser): TVTime User Pydantic Model

        Returns:
            str: task id as hex string
        """
        logger.debug("Scraping Service Started")
        self.redis.add_tvtime_account_to_user(self.user.username, self.tvtime.user.username)
        task = scrape_task.delay(self.tvtime.user)
        return task.id
    
    @classmethod
    def get_status(self, task_id: str) -> dict:
        """Get status of the celery task

        Args:
            task_id (str): celery task id

        Returns:
            dict: response with task id and status
        """
        logger.debug("Task id {task_id}", task_id=task_id)
        result = AsyncResult(id=task_id, app=celery)
        # https://docs.celeryq.dev/en/latest/userguide/tasks.html#built-in-states
        return {"id": result.id, "status": result.status}
