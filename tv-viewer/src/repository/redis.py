from urllib import response
from uuid import UUID
#from redis_om import HashModel
import aioredis

from .storage import Storage
from .schema import User

class RedisStorage(Storage):

    def __init__(self) -> None:
        super().__init__()
        #self.redis = aioredis.from_url("redis://localhost",  username="user", password="pass")
        self.redis = aioredis.from_url("redis://localhost")

    async def get_user(self):
        user =  await self.redis.hgetall(1)
        return user

    async def set_user(self, user:User):
        response = await self.redis.hmset(str(user.account_id), user.dict())
        return response
