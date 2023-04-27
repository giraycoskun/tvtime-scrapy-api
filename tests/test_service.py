import pytest

from src.service.spider import TVTimeSpider

def test_spider():
    spider = TVTimeSpider()
    assert spider.name == "tvtime"
    assert spider.urls == [
        "https://www.tvtime.com/en/upcoming", 
        "https://www.tvtime.com/en/to-watch"
    ]
