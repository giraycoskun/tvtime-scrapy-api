from redis_om import get_redis_connection

from src.config import REDIS_URL
from src.models.data import TVTimeDataModel


class RedisOMClient:
    def __init__(self) -> None:
        self.redis = get_redis_connection(url=REDIS_URL)
        TVTimeDataModel.Meta.database = self.redis
        # try:
        #     Migrator().run()
        # except MigrationError as e:
        #     logger.error(e)

    def exists(self, key):
        key = f"tvtime:data:{key}"
        return self.redis.exists(key)

    def get_ttl(self, key):
        key = f"tvtime:data:{key}"
        return self.redis.ttl(key)

    def get_tvtime_data(self, key):
        user = TVTimeDataModel.get(key)
        return user

    def get_tvtime_watch_next(self, key):
        data = TVTimeDataModel.get(key)
        if "Watch next" in data.to_watch:
            return data.to_watch["Watch next"]
        else:
            return {}

    def get_tvtime_not_watched_for_while(self, key):
        data = TVTimeDataModel.get(key)
        if "Not watched for a while" in data.to_watch:
            return data.to_watch["Not watched for a while"]
        else:
            return {}

    def get_tvtime_not_started_yet(self, key):
        data = TVTimeDataModel.get(key)
        if "Not started yet" in data.to_watch:
            return data.to_watch["Not started yet"]
        else:
            return {}
