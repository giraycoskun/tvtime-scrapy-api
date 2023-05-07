"""Main Initialization of app

Returns:
    FastAPI: tvtime-scrapy-api app
"""

from json import dump

import redis
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from src.config import REDIS_CACHE_URL
from src.routes import scraper, tvtime, user

load_dotenv()

app = FastAPI(
    title="TVTime Scrapy API",
    description="Unofficial TVTime API via Scrapy",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(scraper.router)
app.include_router(tvtime.router)
app.include_router(user.router)


@app.on_event("startup")
async def startup():
    """Startup event for app"""
    redis_client = redis.asyncio.from_url(
        REDIS_CACHE_URL, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")


@cache()
@app.get("/", summary="Hello")
async def root():
    """Root route

    Returns:
        JSONResponse: successful response
    """
    data = {"Hello": "World"}
    return JSONResponse(content=data, status_code=200)


def write_openapi_spec(openapi_app: FastAPI) -> None:
    """Writes OpenAPI spec to file

    Args:
        openapi_app (FastAPI): app with OpenAPI spec
    """
    with open("./docs/assets/openapi.json", "w", encoding="utf-8") as file:
        dump(openapi_app.openapi(), file, indent=4)


# TODO: User route
# TODO: Authentication Scheme
# TODO: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
