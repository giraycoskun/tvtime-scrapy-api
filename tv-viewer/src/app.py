from fastapi import FastAPI
from .repository.schema import User

from .repository.storage import Storage
from logging.config import dictConfig
import logging
from .utils import get_logger, LogConfig

from .repository.redis import RedisStorage

dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")

app = FastAPI(debug=True)


""" @app.on_event("startup")
async def startup_event():
    logger.info(app.state)
    logger.info("Hello World")
    storage = RedisStorage()
    user = User(name="giray", account_id=1)
    await storage.set_user(user)
    response = await storage.get_user()
    logger.info(response)
 """
 
@app.get("/")
async def root():
    logger.info("Test")
    return {"message": "Hello World"}

