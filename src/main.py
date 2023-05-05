from fastapi import FastAPI
from dotenv import load_dotenv
from json import dump

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


@app.get("/", summary="Hello")
async def root():
    return {"Hello": "World"}


def write_openapi_spec(app: FastAPI) -> None:
    with open("./docs/assets/openapi.json", "w") as f:
        dump(app.openapi(), f, indent=4)


# TODO: User route
# TODO: Authentication Scheme
# TODO: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
