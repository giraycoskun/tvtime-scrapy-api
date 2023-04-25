import scrapy
from scrapy.crawler import CrawlerProcess

from dotenv import load_dotenv
from os import environ

load_dotenv()

NUM = 0

class TVTimeSpider(scrapy.Spider):
    name = "tvtime"
    urls = [
        "https://www.tvtime.com/en/upcoming", 
        "https://www.tvtime.com/en/to-watch"
    ]

    def start_requests(self):
        yield scrapy.FormRequest(
            url='https://www.tvtime.com/signin',
            formdata={'username': environ['TVTIME_USERNAME'],
                      'password': environ['TVTIME_PASSWORD']
                      },
            callback=self.logged_in
        )

    def logged_in(self, response):
        print("logged in")
        for url in self.start_urls:
            yield response.follow(url, self.parse)

    def parse(self, response):
        global NUM
        print("#############")
        with open(f'response{NUM}.html', 'wb') as f:
            f.write(response.body)
        NUM += 1

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(TVTimeSpider)
    process.start()

