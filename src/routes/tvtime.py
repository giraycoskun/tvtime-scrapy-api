from fastapi import APIRouter, Response

router = APIRouter(
    prefix="/tvtime",
    tags=["tvtime"],
)

@router.get("/watch-next")
async def get_watch_next() -> Response:
    return Response(status_code=201)
