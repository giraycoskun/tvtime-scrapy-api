import redis
from loguru import logger
from redis_om import get_redis_connection, Migrator, MigrationError, NotFoundError

from src.config import REDIS_URL
from src.repository.models import TVTimeDataModel


class RedisClient:
    def __init__(self):
        self._connection = redis.Redis()
        response = self._connection.ping()
        logger.info(f"Redis Connection: {response}")

    def set_user(self, username):
        self._connection.set('user', username)


class RedisOMClient:
    def __init__(self) -> None:
        self.redis = get_redis_connection(url=REDIS_URL)
        TVTimeDataModel.Meta.database = self.redis
        try:
            Migrator().run()
        except MigrationError as e:
            logger.error(e)

    def exists(self, username):
        try:
            TVTimeDataModel.get(username)
            return True
        except NotFoundError:
            return False

    def get_tvtime_data(self, username):
        user = TVTimeDataModel.get(username)
        return user

    def get_tvtime_towatch(self, username):
        data = TVTimeDataModel.get(username)
        if 'Watch next' in data.to_watch:
            return data.to_watch['Watch next']
        else:
            return {}

    def get_tvtime_not_watched_for_while(self, username):
        data = TVTimeDataModel.get(username)
        if 'Not watched for a while' in data.to_watch:
            return data.to_watch['Not watched for a while']
        else:
            return {}
        
    def get_tvtime_not_started_yet(self, username):
        data = TVTimeDataModel.get(username)
        if 'Not started yet' in data.to_watch:
            return data.to_watch['Not started yet']
        else:
            return {}
