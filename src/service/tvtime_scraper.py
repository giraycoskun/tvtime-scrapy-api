"""TVTime Scraper Service

Returns:
    TVTimeScraperService: Service to handle scraper tasks
"""
from typing import Annotated

from celery.result import AsyncResult
from fastapi import Depends
from loguru import logger

from src.models.api import TVTimeUser
from src.repository.celery_repository import celery, scrape_task
from src.repository.redis_repository import RedisOMClient


class TVTimeScraperService:
    def __init__(self, redis_client: Annotated[RedisOMClient, Depends()]):
        self.celery = celery
        self.redis = redis_client

    def scrape(self, user: TVTimeUser) -> str:
        logger.debug("Scraping Service Started")
        task = scrape_task.delay(user)
        return task.id

    def get_status(self, task_id):
        logger.debug("Task id {task_id}", task_id=task_id)
        result = AsyncResult(id=task_id, app=self.celery)
        # https://docs.celeryq.dev/en/latest/userguide/tasks.html#built-in-states
        return {"id": result.id, "status": result.status}
