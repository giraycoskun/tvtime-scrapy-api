from pydantic import BaseModel
from redis_om import EmbeddedJsonModel, Field
from typing import Optional
from os import environ
from dotenv import load_dotenv

load_dotenv()

class TVTimeUser(BaseModel):
    username: str
    password: str

class TVTimeDataModel(EmbeddedJsonModel):
    username: str=Field(index=True, primary_key=True)
    user_id: Optional[str]
    to_watch: Optional[dict]
    upcoming: Optional[dict]

    class Meta:
        global_key_prefix = "tvtime"
        model_key_prefix = "data"