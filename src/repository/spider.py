import scrapy
from scrapy.crawler import CrawlerProcess
import json
from dotenv import load_dotenv
from os import environ
import re
from loguru import logger
from redis_om import get_redis_connection

from src.repository.models import TVTimeDataModel, TVTimeUser
from src.config import REDIS_URL

load_dotenv()


class TVTimeSpider(scrapy.Spider):

    name = "tvtime"
    TO_WATCH_URL = "https://www.tvtime.com/en/to-watch"
    UPCOMING_URL = "https://www.tvtime.com/en/upcoming"
    TVTIME_PROFILE_URL = "https://www.tvtime.com/en/user/"

    def __init__(self, user:TVTimeUser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def start_requests(self):
        yield scrapy.FormRequest(
            url='https://www.tvtime.com/signin',
            formdata={'username': self.user.username,
                      'password': self.user.password,
                      },
            callback=self.logged_in
        )

    def logged_in(self, response):
        script_content = response.selector.xpath('/html/head/script[contains(text(), "tvst.user")]/text()').get()
        user_id = int(re.search(r'(?<= id:[ ]")[0-9]*', script_content).group(0))
        yield {'name':'id', 'data': {'user_id': user_id}}
        yield response.follow(self.TO_WATCH_URL, self.parse_to_watch)
        yield response.follow(self.UPCOMING_URL, self.parse_upcoming)
        yield scrapy.Request(f"{self.TVTIME_PROFILE_URL}/{user_id}/profile", self.parse_profile)
    
    def parse_to_watch(self, response):
        result = {'name': 'to-watch', 'data': {}}
        items = response.selector.xpath('//*[@id="to-watch"]/ul')
        title_not_watched = items[0].xpath('.//img/@alt').getall()
        title_not_started = items[1].xpath('.//img/@alt').getall()
        result['data']['not-watched'] = title_not_watched
        result['data']['not-started'] = title_not_started
        return result
    
    def parse_upcoming(self, response):
        result = {'name': 'upcoming', 'data': {}}
        items = response.selector.xpath('//*[@id="upcoming-episodes"]/ul/li')
        for item in items:
            title =item.xpath('.//div[@class="episode-details poster-details"]/a/text()').get()
            episode =  item.xpath('//*[@id="upcoming-episodes"]/ul/li/div[@class="episode-details poster-details"]/h2/a/text()').get()
            day = item.xpath('.//div[@class="overlay"]//ul/li/div/text()').get()
            if title:
                result['data'][title] = {episode: day}
        return result
    
    def parse_profile(self, response):
        pass
    

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
    

class RedisWriterPipeline:

    def __init__(self, user) -> None:
        self.redis = get_redis_connection(url=REDIS_URL)
        TVTimeDataModel.Meta.database = self.redis
        self.username = user.username
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.spider.user) 

    def open_spider(self, spider):
        logger.debug(f"Opening spider {spider.name}")
        self.data = TVTimeDataModel(username=self.username)
        self.data.save()
        logger.debug(f"Data model created {self.data.pk}")

    def process_item(self, item, spider):
        logger.debug(f"Processing item {item}")
        name = item.get('name')
        if name == 'id':
            self.data.user_id = item.get('data').get('user_id')
        elif name == 'to-watch':
            self.data.to_watch = item.get('data')
        elif name == 'upcoming':
            self.data.upcoming = item.get('data')
        self.data.save()

    def close_spider(self, spider):
        logger.debug(f"Closing spider {spider.name}")
        self.redis.close()


if __name__ == "__main__":

    process = CrawlerProcess(settings={
        "ITEM_PIPELINES": {
            "src.repository.spider.RedisWriterPipeline": 1,
        }
    })
    input_args = {"username": environ['TVTIME_USERNAME'], "password": environ['TVTIME_PASSWORD']}
    process.crawl(TVTimeSpider, **input_args)
    process.start()
    