import pytest

from src.repository.spider import TVTimeSpider
from src.repository.models import TVTimeUser

def test_spider():
    user = TVTimeUser(username="test", password="test")
    spider = TVTimeSpider(user)
    assert spider.name == "tvtime"
