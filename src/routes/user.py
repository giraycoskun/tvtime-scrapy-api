from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={
        200: {"description": "Success"},
    },
)

@router.get("", summary="Get Data Status")
def get_user():
    data = {"status": "not implemented"}
    return JSONResponse(content=data, status_code=200)

