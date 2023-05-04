from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Annotated

from src.service.tvtime_data import TVTimeDataService

#TODO: Update to async routes

router = APIRouter(
    prefix="",
    tags=["tvtime"],
    responses={
        200: {"description": "Success"},
    },
)


@router.get("/status", summary="Get Data Status")
def get_status(username: str, tvtime_data_service: Annotated[TVTimeDataService, Depends()]):
    response = tvtime_data_service.get_status(username)
    return JSONResponse(content=response, status_code=200)


@router.get("/all-data", summary="Get All Data")
def get_all_data(username: str, tvtime_data_service: Annotated[TVTimeDataService, Depends()]):
    data = tvtime_data_service.get_all_data(username)
    return JSONResponse(content=data.dict(), status_code=200)


@router.get("/watch-next", summary="Get Watch Next List")
def get_watch_next(username: str, tvtime_data_service: Annotated[TVTimeDataService, Depends()]):
    data = tvtime_data_service.get_watch_next(username)
    return JSONResponse(content=data, status_code=200)

@router.get("/not-watched-for-while", summary="Get Not Watched For While List")
def get_not_watched_for_while(username: str, tvtime_data_service: Annotated[TVTimeDataService, Depends()]):
    data = tvtime_data_service.get_not_watched_for_while(username)
    return JSONResponse(content=data, status_code=200)

@router.get("/not-started-yet", summary="Get Not Started Yet List")
def get_not_started_yet(username: str, tvtime_data_service: Annotated[TVTimeDataService, Depends()]):
    data = tvtime_data_service.get_not_started_yet(username)
    return JSONResponse(content=data, status_code=200)

