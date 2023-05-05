from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated
from loguru import logger
from redis.exceptions import ConnectionError
from src.repository.models import Show, Season, Episode, TVTimeUser

from src.service.tvtime_data import TVTimeDataService

# TODO: Update to async routes

router = APIRouter(
    prefix="",
    tags=["tvtime"],
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found/Redis Connection Error"},
    },
)


@router.get("/status", summary="Get Data Status")
def get_status(
    username: str, tvtime_data_service: Annotated[TVTimeDataService, Depends()]
):
    try:
        response = tvtime_data_service.get_status(username)
    except ConnectionError as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Redis Connection Error")
    return JSONResponse(content=response, status_code=200)


@router.get("/all-data", summary="Get All Data")
def get_all_data(
    username: str, tvtime_data_service: Annotated[TVTimeDataService, Depends()]
):
    try:
        data = tvtime_data_service.get_all_data(username)
    except ConnectionError as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Redis Connection Error")
    return JSONResponse(content=data.dict(), status_code=200)


@router.get("/watch-next", summary="Get Watch Next List")
def get_watch_next(
    username: str, tvtime_data_service: Annotated[TVTimeDataService, Depends()]
):
    try:
        response = tvtime_data_service.get_watch_next(username)
    except ConnectionError as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Redis Connection Error")
    return JSONResponse(content=response, status_code=200)


@router.get("/not-watched-for-while", summary="Get Not Watched For While List")
def get_not_watched_for_while(
    username: str, tvtime_data_service: Annotated[TVTimeDataService, Depends()]
):
    try:
        response = tvtime_data_service.get_not_watched_for_while(username)
    except ConnectionError as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Redis Connection Error")
    return JSONResponse(content=response, status_code=200)


@router.get("/not-started-yet", summary="Get Not Started Yet List")
def get_not_started_yet(
    username: str, tvtime_data_service: Annotated[TVTimeDataService, Depends()]
):
    try:
        response = tvtime_data_service.get_not_started_yet(username)
    except ConnectionError as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="Redis Connection Error")
    return JSONResponse(content=response, status_code=200)


@router.get("/show", summary="Get Show")
def get_show(
    username: str,
    show: Show,
    tvtime_data_service: Annotated[TVTimeDataService, Depends()],
):
    response = {"message": "Not Impemented"}
    return JSONResponse(content=response, status_code=501)


@router.put("/show", summary="Follow a show")
def follow_show(user: TVTimeUser, show: Show):
    response = {"message": "Not Impemented"}
    return JSONResponse(content=response, status_code=501)


@router.delete("/show", summary="Unfollow a show")
def unfollow_show(user: TVTimeUser, show: Show):
    response = {"message": "Not Impemented"}
    return JSONResponse(content=response, status_code=501)


@router.put("/show/until", summary="Mark show as watched until a date")
def mark_show_watched_until(user: TVTimeUser, show: Show):
    response = {"message": "Not Impemented"}
    return JSONResponse(content=response, status_code=501)


@router.put("/episode", summary="Mark Episode Watched")
def mark_episode_watched(
    user: TVTimeUser,
    episode: Episode,
    tvtime_data_service: Annotated[TVTimeDataService, Depends()],
):
    response = {"message": "Not Impemented"}
    return JSONResponse(content=response, status_code=501)


@router.delete("/episode", summary="Mark Episode UnWatched")
def mark_episode_unwatched(
    user: TVTimeUser,
    episode: Episode,
    tvtime_data_service: Annotated[TVTimeDataService, Depends()],
):
    response = {"message": "Not Impemented"}
    return JSONResponse(content=response, status_code=501)


@router.put("/season", summary="Mark Season Watched")
def mark_season_watched(
    user: TVTimeUser,
    season: Season,
    tvtime_data_service: Annotated[TVTimeDataService, Depends()],
):
    response = {"message": "Not Impemented"}
    return JSONResponse(content=response, status_code=501)


@router.delete("/season", summary="Mark Season UnWatched")
def mark_season_watched(
    user: TVTimeUser,
    season: Season,
    tvtime_data_service: Annotated[TVTimeDataService, Depends()],
):
    response = {"message": "Not Impemented"}
    return JSONResponse(content=response, status_code=501)
