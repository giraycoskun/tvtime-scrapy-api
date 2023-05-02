import scrapy
from scrapy.crawler import CrawlerProcess
import json
from dotenv import load_dotenv
from os import environ
import re
from loguru import logger
from redis_om import get_redis_connection, Migrator

from src.repository.models import TVTimeDataModel, TVTimeUser
from src.config import REDIS_URL

load_dotenv()


class TVTimeSpider(scrapy.Spider):

    name = "tvtime"
    TO_WATCH_URL = "https://www.tvtime.com/en/to-watch"
    UPCOMING_URL = "https://www.tvtime.com/en/upcoming"
    TVTIME_PROFILE_URL = "https://www.tvtime.com/en/user/"

    def __init__(self, user: TVTimeUser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        logger.info(f"User: {user}")

    def start_requests(self):
        logger.info(f"Starting Requests for {self.user.username}")
        yield scrapy.FormRequest(
            url='https://www.tvtime.com/signin',
            formdata={'username': self.user.username,
                      'password': self.user.password,
                      },
            callback=self.logged_in
        )

    def logged_in(self, response):
        script_content = response.selector.xpath(
            '/html/head/script[contains(text(), "tvst.user")]/text()').get()
        user_id = int(
            re.search(r'(?<= id:[ ]")[0-9]*', script_content).group(0))
        yield {'name': 'id', 'data': {'user_id': user_id}}
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
        # script_content = response.selector.xpath('//div[@class="main-block-container"]/script/text()').get()
        # data_content = re.search(r'(tvst.data = )(.*)(;)', script_content, re.DOTALL).group(2)
        # data_content = data_content.replace('\&quot;', ' ')
        # data_content = data_content.replace("'", "")
        # data_content = data_content.replace('evt:', '')
        # data_content = data_content.replace('//', '')
        # data_content = data_content.replace("\&quot;", '"').replace("'[", "[").replace("]'", "]").replace('toWatchEpisodes', '"toWatchEpisodes"').replace('trendingShows', '"trendingShows"').replace('evt', '"evt"')
        # data_content = data_content.replace('\\"', '').replace('\\', '').replace("'", '"')
        # with open('data.json', 'w') as f:
        #     f.write(data_content)
        # data = json.loads(data_content)
        return result

    def parse_upcoming(self, response):
        result = {'name': 'upcoming', 'data': {}}
        items = response.selector.xpath('//*[@id="upcoming-episodes"]/ul/li')
        for item in items:
            title = item.xpath(
                './/div[@class="episode-details poster-details"]/a/text()').get()
            episode = item.xpath(
                '//*[@id="upcoming-episodes"]/ul/li/div[@class="episode-details poster-details"]/h2/a/text()').get()
            day = item.xpath(
                './/div[@class="overlay"]//ul/li/div/text()').get()
            if title:
                result['data'][title] = {episode: day}
        return result

    def parse_profile(self, response):
        result = {'name': 'profile', 'data': {}}
        script_content = response.selector.xpath(
            '//div[@class="main-block-container"]/script/text()').get()
        data_content = re.search(
            r'(tvst.data = )(.*)(;)', script_content, re.DOTALL).group(2)
        data_content = data_content.replace('\&quot;', '"').replace('shows', '"shows"', 1).replace(
            'profile', '"profile"', 1).replace("'[", "[").replace("]'", "]").replace("'{", "{").replace("}'", "}").replace("\&", "")
        with open('data.json', 'w') as f:
            f.write(data_content)
        result['data'] = json.loads(data_content)
        return result


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
        self.username = user.username
        TVTimeDataModel.Meta.database = get_redis_connection(url=REDIS_URL)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.spider.user)

    def open_spider(self, spider):
        logger.debug(f"Opening spider {spider.name}")
        self.data = TVTimeDataModel(username=self.username)
        self.data.save()

    def process_item(self, item, spider):
        logger.debug(f"Processing item {item}")
        name = item.get('name')
        if name == 'id':
            self.data.user_id = item.get('data').get('user_id')
        elif name == 'to-watch':
            self.data.to_watch = item.get('data')
        elif name == 'upcoming':
            self.data.upcoming = item.get('data')
        elif name == 'profile':
            self.data.profile = item.get('data')

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
    user = TVTimeUser(
        username=environ['TVTIME_USERNAME'], password=environ['TVTIME_PASSWORD'])
    input_args = {"user": user}
    process.crawl(TVTimeSpider, **input_args)
    process.start()
