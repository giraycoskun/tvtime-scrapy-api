import scrapy
from scrapy.crawler import CrawlerProcess
import json
from dotenv import load_dotenv
from os import environ
import re

load_dotenv()


class TVTimeSpider(scrapy.Spider):

    name = "tvtime"
    TO_WATCH_URL = "https://www.tvtime.com/en/to-watch"
    UPCOMING_URL = "https://www.tvtime.com/en/upcoming"
    TVTIME_PROFILE_URL = "https://www.tvtime.com/en/user/"

    def start_requests(self):
        yield scrapy.FormRequest(
            url='https://www.tvtime.com/signin',
            formdata={'username': environ['TVTIME_USERNAME'],
                      'password': environ['TVTIME_PASSWORD']
                      },
            callback=self.logged_in
        )

    def logged_in(self, response):
        script_content = response.selector.xpath('/html/head/script[contains(text(), "tvst.user")]/text()').get()
        user_id = int(re.search(r'(?<= id:[ ]")[0-9]*', script_content).group(0))
        yield {'user_id': user_id}
        yield response.follow(self.TO_WATCH_URL, self.parse_to_watch)
        yield response.follow(self.UPCOMING_URL, self.parse_upcoming)
        yield scrapy.Request(f"{self.TVTIME_PROFILE_URL}/{user_id}/profile", self.parse_profile)
    
    def parse_to_watch(self, response):
        items = response.selector.xpath('//*[@id="to-watch"]/ul')
        title_not_watched = items[0].xpath('.//img/@alt').getall()
        title_not_started = items[1].xpath('.//img/@alt').getall()
        return {
            'title_not_watched': title_not_watched,
            'title_not_started': title_not_started
        }
    
    def parse_upcoming(self, response):
        data = {}
        items = response.selector.xpath('//*[@id="upcoming-episodes"]/ul/li')
        for item in items:
            title =item.xpath('.//div[@class="episode-details poster-details"]/a/text()').get()
            episode =  item.xpath('//*[@id="upcoming-episodes"]/ul/li/div[@class="episode-details poster-details"]/h2/a/text()').get()
            day = item.xpath('.//div[@class="overlay"]//ul/li/div/text()').get()
            if title:
                data[title] = {episode: day}
        return data
    
    def parse_profile(self, response):
        with open('response.html', 'wb') as f:
            f.write(response.body)
    

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "ITEM_PIPELINES": {
            "src.service.spider.JsonWriterPipeline": 1,
        }
    })
    process.crawl(TVTimeSpider)
    process.start()

'''with open('response1.html', 'r') as f:
    response = f.read()

    selector = scrapy.Selector(text=response)
    items = selector.xpath('//*[@id="to-watch"]/ul')
    for item in items:
        title = item.xpath('.//img/@alt').getall()
        episode = item.xpath('.//div[@class="episode-details poster-details"]/h2/a/text()').getall()
        remaining = item.xpath('.//div[@class="episode-details poster-details"]/text()').getall() 
        remainings = [i.strip() for i in remaining if i.strip() != '']
        urls = item.xpath('.//div[@class="image-crop"]/a/@href').getall()
        print(title)

    print("#############")'''
