import redis
from loguru import logger

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
