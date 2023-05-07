"""_summary_

Raises:
    HTTPException: Redis Connection Error
    HTTPException: Celery Operational Error

Returns:
    APIRouter: Router to scrape tvtime
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from kombu.exceptions import OperationalError
from loguru import logger
from redis.exceptions import ConnectionError as RedisConnectionError

from src.models.api import TVTimeUser
from src.service.tvtime_scraper import TVTimeScraperService

router = APIRouter(
    prefix="/scraper",
    tags=["scraper"],
    responses={
        200: {"description": "Success"},
        204: {"description": "Scrape Task Accepted"},
        404: {"description": "Not found"},
    },
)


@router.post("/", summary="Start Scrape Task")
def start_scrape(
    user: TVTimeUser, tvtime_scraper_service: Annotated[TVTimeScraperService, Depends()]
) -> Response:
    try:
        task_id = tvtime_scraper_service.scrape(user)
        data = {"status": "success", "task_id": task_id}
    except OperationalError as exc:
        logger.error(exc)
        raise HTTPException(status_code=404, detail="Celery Operational Error") from exc
    return JSONResponse(content=data, status_code=202)


@router.get("/{task_id}", summary="Scrape Task Status")
def scrape_status(
    task_id: str, tvtime_scraper_service: Annotated[TVTimeScraperService, Depends()]
) -> Response:
    """_summary_

    Args:
        task_id (str): Celery Task ID
        tvtime_scraper_service (Annotated[TVTimeScraperService, Depends): TVTimeScraperService

    Returns:
        Response: status of the celery task
    """
    try:
        data = tvtime_scraper_service.get_status(task_id)
    except RedisConnectionError as exc:
        logger.error(exc)
        raise HTTPException(status_code=404, detail="Redis Connection Error") from exc
    return JSONResponse(content=data, status_code=200)
