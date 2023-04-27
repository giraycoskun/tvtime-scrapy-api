from fastapi import APIRouter, Response, BackgroundTasks, Depends
from typing import Annotated
from pydantic import BaseModel

from src.service.tvtime import TVService

router = APIRouter(
    prefix="/tvtime",
    tags=["tvtime"],
    responses={
        201: {"description": "Created"},
        404: {"description": "Not found"}
    },
)


class TVTimeUser(BaseModel):
    username: str
    password: str


@router.post("/scrape")
def scrape(user: TVTimeUser, tvtime_service: Annotated[TVService, Depends()], background_tasks: BackgroundTasks) -> Response:
    background_tasks.add_task(tvtime_service.scrape, user)
    return Response(status_code=201)


@router.get("/watch-next")
async def get_watch_next() -> Response:
    return Response(status_code=201)
