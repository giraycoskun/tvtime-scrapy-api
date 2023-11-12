from uuid import UUID

from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    user_id: str
    username: str
    is_active: bool = True
    is_admin: bool = False


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
