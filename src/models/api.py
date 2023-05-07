from uuid import UUID

from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    user_id: UUID
    username: str
    tv_time_username: str
    disabled: bool | None = None


class UserDB(UserOut):
    hashed_password: str


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
