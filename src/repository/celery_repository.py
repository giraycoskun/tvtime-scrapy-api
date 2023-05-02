from loguru import logger
from celery import Celery
import os
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor

from src.repository.spider import TVTimeSpider
from src.repository.models import TVTimeUser

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379")
celery.conf.task_serializer = 'pickle'
celery.conf.accept_content = ['pickle', 'json']
celery.conf.worker_max_tasks_per_child = 1

@celery.task(name="scrape_task")
def scrape_task(user: TVTimeUser):
    logger.info(f"Scraping Task Started")
    logger.debug(f"User: {user}")
    logger.debug(f"User: {user.username}")
    spider_process = CrawlerProcess(settings={
        "ITEM_PIPELINES": {
            "src.repository.spider.RedisWriterPipeline": 1,
        }
    })
    input_args = {"user": user}
    spider_process.crawl(TVTimeSpider, **input_args)
    spider_process.start()
