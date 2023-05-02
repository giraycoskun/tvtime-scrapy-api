from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Annotated

from src.service.tvtime_data import TVTimeDataService

router = APIRouter(
    prefix="/data",
    tags=["data"],
    responses={
        200: {"description": "Success"},
    },
)

@router.get("/status", summary="Get Data Status")
def get_status():
    data = {"status": "not implemented"}
    return JSONResponse(content=data, status_code=200)

@router.get("/all", summary="Get All Data")
def get_data(tvtime_data_serive: Annotated[TVTimeDataService, Depends()]):
    data  = tvtime_data_serive.get_all_data('giraycoskundev')
    return JSONResponse(content=data.dict(), status_code=200)
    

@router.get("/to_watch", summary="Get To Watch List")
def get_to_watch():
    data = {"status": "not implemented"}
    return JSONResponse(content=data, status_code=200)
