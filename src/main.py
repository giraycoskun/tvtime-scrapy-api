from fastapi import FastAPI
from dotenv import load_dotenv

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

openapi_spec = app.openapi()
print(openapi_spec)
