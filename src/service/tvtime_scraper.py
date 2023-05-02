from loguru import logger
from fastapi import Depends
from typing import Annotated

from src.repository.celery_repository import scrape_task, celery
from src.repository.redis_repository import RedisClient
from src.repository.models import TVTimeUser

class TVTimeScraperService:

    def __init__(self, redis_client: Annotated[RedisClient, Depends()]):
        self.celery = celery
        self.redis = redis_client

    def scrape(self, user:TVTimeUser) -> str:
        logger.debug(f"Scraping Service Started")
        task = scrape_task.delay(user)
        return task.id

    def get_status(self, task_id):
        logger.debug("Task id {task_id}", task_id=task_id)
        result = result.AsyncResult(id=task_id, app=self.celery)
        # https://docs.celeryq.dev/en/latest/userguide/tasks.html#built-in-states
        return {
            "id": result.id,
            "status": result.status
        }
