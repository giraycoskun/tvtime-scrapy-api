import pytest

from src.repository.spider import TVTimeSpider

def test_spider():
    spider = TVTimeSpider()
    assert spider.name == "tvtime"
