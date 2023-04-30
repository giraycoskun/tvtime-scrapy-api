from fastapi import APIRouter, Response, Depends
from typing import Annotated

from src.repository.models import TVTimeUser
from src.service.tvtime import TVTimeService

router = APIRouter(
    prefix="/tvtime",
    tags=["tvtime"],
    responses={
        201: {"description": "Created"},
        404: {"description": "Not found"}
    },
)


@router.post("/scrape", summary="POST Scrape Task")
def scrape(user: TVTimeUser, tvtime_service: Annotated[TVTimeService, Depends()]) -> Response:
    task_id = tvtime_service.scrape(user)
    return {
        "status": "success",
        "task_id": task_id
    }


@router.get("/scrape", summary="GET Scrape Task Status")
def scrape(task_id: str, tvtime_service: Annotated[TVTimeService, Depends()]) -> Response:
    response = tvtime_service.get_status(task_id)
    return response


@router.get("/watch-next")
async def get_watch_next() -> Response:
    return Response(status_code=201)
