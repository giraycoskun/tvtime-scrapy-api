import redis
from loguru import logger
from redis_om import get_redis_connection, Migrator, MigrationError

from src.config import REDIS_URL
from src.repository.models import TVTimeDataModel

class RedisClient:
    def __init__(self):
        self._connection = redis.Redis()
        response = self._connection.ping()
        logger.info(f"Redis Connection: {response}")

    def set_user(self, username):
        self._connection.set('user', username)

if __name__ == "__main__":
    redis_client = RedisClient("localhost", 6379, 0)
    redis_client.set_user("test2")

class RedisOMClient:
    def __init__(self) -> None:
        self.redis = get_redis_connection(url=REDIS_URL)
        TVTimeDataModel.Meta.database = self.redis
        try:
            Migrator().run()
        except MigrationError as e:
            logger.error(e)


    def get_tvtime_data(self, username):
        user = TVTimeDataModel.get(username)
        return user