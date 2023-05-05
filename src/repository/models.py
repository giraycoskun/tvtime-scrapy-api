from pydantic import BaseModel
from redis_om import Field, JsonModel
from typing import Optional
from os import environ
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


class TVTimeUser(BaseModel):
    username: str
    password: str


class Show(BaseModel):
    show_id: int


class Episode(BaseModel):
    episode_id: int


class Season(BaseModel):
    season: int
    show: Show


class TVTimeDataModel(JsonModel):
    username: str = Field(index=True, primary_key=True)
    user_id: Optional[str]
    to_watch: Optional[dict]
    upcoming: Optional[dict]
    profile: Optional[dict]

    class Meta:
        global_key_prefix = "tvtime"
        model_key_prefix = "data"
