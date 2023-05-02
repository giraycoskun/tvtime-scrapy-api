from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Annotated

from src.service.tvtime_data import TVTimeDataService

router = APIRouter(
    prefix="",
    tags=["tvtime"],
    responses={
        200: {"description": "Success"},
    },
)


@router.get("/status", summary="Get Data Status")
def get_status(username: str, tvtime_data_serive: Annotated[TVTimeDataService, Depends()]):
    response = tvtime_data_serive.get_status(username)
    data = {"exists": response}
    return JSONResponse(content=data, status_code=200)


@router.get("/all", summary="Get All Data")
def get_data(username: str, tvtime_data_serive: Annotated[TVTimeDataService, Depends()]):
    data = tvtime_data_serive.get_all_data(username)
    return JSONResponse(content=data.dict(), status_code=200)


@router.get("/to_watch", summary="Get To Watch List")
def get_to_watch(username: str, tvtime_data_serive: Annotated[TVTimeDataService, Depends()]):
    data = tvtime_data_serive.get_watch_next(username)
    return JSONResponse(content=data, status_code=200)

@router.get("/not_watched_for_while", summary="Get Not Watched For While List")
def get_not_watched_for_while(username: str, tvtime_data_serive: Annotated[TVTimeDataService, Depends()]):
    data = tvtime_data_serive.get_not_watched_for_while(username)
    return JSONResponse(content=data, status_code=200)

@router.get("/not_started_yet", summary="Get Not Started Yet List")
def get_not_started_yet(username: str, tvtime_data_serive: Annotated[TVTimeDataService, Depends()]):
    data = tvtime_data_serive.get_not_started_yet(username)
    return JSONResponse(content=data, status_code=200)

