import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
import json
from dotenv import load_dotenv
import re
from loguru import logger
from redis_om import get_redis_connection

from src.repository.models import TVTimeDataModel, TVTimeUser
from src.config import REDIS_URL, TVTIME_TOWATCH_URL, TVTIME_PROFILE_URL, TVTIME_UPCOMING_URL

load_dotenv()


class TVTimeSpider(scrapy.Spider):
    name = "tvtime"
    USER_NOTFOUND_FLAG = False

    def __init__(self, user: TVTimeUser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        logger.info(f"User: {user}")

    def start_requests(self):
        logger.info(f"Starting Requests for {self.user.username}")
        yield scrapy.FormRequest(
            url="https://www.tvtime.com/signin",
            formdata={
                "username": self.user.username,
                "password": self.user.password,
            },
            callback=self.logged_in,
        )

    def logged_in(self, response):
        logger.debug(f"Logged in {self.user.username}")
        script_content = response.selector.xpath(
            '/html/head/script[contains(text(), "tvst.user")]/text()'
        ).get()
        user_id = re.search(r'(?<= id:[ ]")[0-9]*', script_content).group(0)
        if user_id == "":
            logger.error("User not found")
            self.USER_NOTFOUND_FLAG = True
            raise CloseSpider("User not found")
        user_id = int(user_id)
        yield {"name": "id", "data": {"user_id": user_id}}
        yield response.follow(TVTIME_TOWATCH_URL, self.parse_to_watch)
        yield response.follow(TVTIME_UPCOMING_URL, self.parse_upcoming)
        yield scrapy.Request(
            f"{TVTIME_PROFILE_URL}/{user_id}/profile", self.parse_profile
        )

    def parse_to_watch(self, response):
        result = {"name": "to-watch", "data": {}}
        items = response.selector.xpath('//*[@id="to-watch"]/ul')
        titles = response.selector.xpath('//*[@id="to-watch"]/h1')
        for idx in range(len(items)):
            title = titles[idx].xpath("./text()").get().strip()
            result["data"][title] = {}
            new_tags = items[idx].xpath('.//div[@class="new-label"]/text()').getall()
            shows = items[idx].xpath(".//img/@alt").getall()
            episodes = (
                items[idx]
                .xpath('.//div[@class="episode-details poster-details"]/h2/a/text()')
                .getall()
            )
            for show, episode in zip(shows, episodes):
                tag = False
                if len(new_tags) > 0:
                    tag = True
                    new_tags.pop(0)
                temp = {"episode": episode, "is_new": tag}
                result["data"][title][show] = temp

        # title_not_watched = items[0].xpath('.//img/@alt').getall()
        # title_not_started = items[1].xpath('.//img/@alt').getall()
        # result['data']['not-watched'] = title_not_watched
        # result['data']['not-started'] = title_not_started
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
        result = {"name": "upcoming", "data": {}}
        items = response.selector.xpath('//*[@id="upcoming-episodes"]/ul/li')
        for item in items:
            title = item.xpath(
                './/div[@class="episode-details poster-details"]/a/text()'
            ).get()
            episode = item.xpath(
                '//*[@id="upcoming-episodes"]/ul/li/div[@class="episode-details poster-details"]/h2/a/text()'
            ).get()
            day = item.xpath('.//div[@class="overlay"]//ul/li/div/text()').get()
            if title:
                result["data"][title] = {episode: day}
        return result

    def parse_profile(self, response):
        result = {"name": "profile", "data": {}}
        script_content = response.selector.xpath(
            '//div[@class="main-block-container"]/script/text()'
        ).get()
        data_content = re.search(
            r"(tvst.data = )(.*)(;)", script_content, re.DOTALL
        ).group(2)
        data_content = (
            data_content.replace("\&quot;", '"')
            .replace("shows", '"shows"', 1)
            .replace("profile", '"profile"', 1)
            .replace("'[", "[")
            .replace("]'", "]")
            .replace("'{", "{")
            .replace("}'", "}")
            .replace("\&", "")
        )
        with open("data.json", "w") as f:
            f.write(data_content)
        result["data"] = json.loads(data_content)
        return result


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open("items.json", "w")

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
        self.data.expire(86400)

    def process_item(self, item, spider):
        logger.debug(f"Processing item {item}")
        name = item.get("name")
        if name == "id":
            self.data.user_id = item.get("data").get("user_id")
        elif name == "to-watch":
            self.data.watch_next = item.get("data")
        elif name == "upcoming":
            self.data.upcoming = item.get("data")
        elif name == "profile":
            self.data.profile = item.get("data")
        self.data.save()

    def close_spider(self, spider):
        logger.debug(f"Closing spider {spider.name}")
        if spider.USER_NOTFOUND_FLAG:
            self.data.expire(0)
        self.redis.close()


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "ITEM_PIPELINES": {
                "src.repository.spider.RedisWriterPipeline": 1,
            }
        }
    )
    user = TVTimeUser(username="string", password="string")
    input_args = {"user": user}
    process.crawl(TVTimeSpider, **input_args)
    process.start()
