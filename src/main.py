from fastapi import FastAPI
from dotenv import load_dotenv
from json import dump
from celery import Celery
import os

from src.routes import tvtime

load_dotenv()

app = FastAPI(
    title="TVTime Scrapy API",
    description="Unofficial TVTime API via Scrapy",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(tvtime.router)


@app.get("/")
async def root():
    return {"Hello": "World"}


def write_openapi_spec(app : FastAPI) -> None:
    with open("./docs/assets/openapi.json", "w") as f:
        dump(app.openapi(), f, indent=4)
        