import pytest

from src.service.spider import TVTimeSpider

def test_spider():
    spider = TVTimeSpider()
    assert spider.name == "tvtime"
