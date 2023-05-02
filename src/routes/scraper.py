from fastapi import APIRouter, Response, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated

from src.repository.models import TVTimeUser
from src.service.tvtime_scraper import TVTimeScraperService

router = APIRouter(
    prefix="/scraper",
    tags=["scraper"],
    responses={
        200: {"description": "Success"},
        204: {"description": "Scrape Task Accepted"},
        404: {"description": "Not found"}
    },
)


@router.post("/scrape", summary="Start Scrape Task")
def start_scrape(user: TVTimeUser, tvtime_scraper_service: Annotated[TVTimeScraperService, Depends()]) -> Response:
    task_id = tvtime_scraper_service.scrape(user)
    data = {
        "status": "success",
        "task_id": task_id
    }
    return JSONResponse(content=data, status_code=202)

@router.get("/scrape", summary="Scrape Task Status")
def scrape_status(task_id: str, tvtime_scraper_service: Annotated[TVTimeScraperService, Depends()]) -> Response:
    """_summary_

    Args:
        task_id (str): _description_
        tvtime_service (Annotated[TVTimeService, Depends): _description_

    Returns:
        Response: _description_
    """    
    data = tvtime_scraper_service.get_status(task_id)
    return JSONResponse(content=data, status_code=200)
