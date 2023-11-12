from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    account_id: int

    class Config:
        orm_mode = True