from urllib import response
from requests import Request, Session
from loguru import logger
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
from lxml import html
from enum import Enum, unique
from tv_service import TVService

load_dotenv()

class TvTime(TVService):

    TV_TIME_HOST = "www.tvtime.com"
    TVTIME_URL = f"https://{TV_TIME_HOST}/"
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    DOWNLOAD_DIR = "./src/html/"

    def __init__(self, user, download_flag=True) -> None:
        super().__init__()
        self.user = user

        self.download_flag = download_flag
        if download_flag and (not os.path.exists(self.DOWNLOAD_DIR)):
            os.makedirs(self.DOWNLOAD_DIR)

        self.session = Session()
        headers = {
            "User-Agent":self.USER_AGENT,
            "Host": self.TV_TIME_HOST
        }
        self.session.headers.update(headers)
        self.parser = TvTimeParser()

    def sign_in(self):
        url = self.TVTIME_URL + 'signin'
        payload = {'username': os.environ['TV_TIME_USERNAME'],
                   'password': os.environ['TV_TIME_PASSWORD'],
                   'redirect_path': 'https://www.tvtime.com/en/to-watch'}
        response = self.session.post(url=url, data=payload)
        logger.debug(response)

        if self.download_flag:
            output = response.text
            filename = self.DOWNLOAD_DIR + 'home'
            with open(filename, 'w') as file:
                file.write(output)

    def sign_out(self):
        url = self.TVTIME_URL + 'signout'
        response = self.session.get(url=url)
        logger.debug(response)
        self.session.close()

    def get_home_page(self):
        url = self.TVTIME_URL + 'en'
        response = self.session.get(url=url)
        

    def get_watching_shows():
        pass

    def get_upcoming_shows():
        pass

class TvTimeParser:

    @unique
    class TvTimeLinks(Enum):
        HomeLink = 'home'
        ProfileLink = 'profile'
        UpcomingLink = 'upcoming'
        CalendarLink = 'calendar'

    def __init__(self) -> None:
        self.parser_name = "html5lib"
        self.links_map = {}
        self.soups = {}
        self.element_trees = {}

    def get_link(self, link):
        if link in self.links_map:
            return self.links_map[link]
        else:
            #page = get_
            etree = html.fromstring(page)
            self.element_trees['home'] = etree
        profile_link = etree.xpath('//*[@id="menu"]/ul/li[4]/a')
        upcoming_link = etree.xpath('//*[@id="menu"]/ul/li[2]/a')


if __name__ == '__main__':
    logger.info(os.getcwd())
    logger.info("Program Starts")
    user = {
        'username': os.environ['TV_TIME_USERNAME'],
        'password': os.environ['TV_TIME_PASSWORD']
    }
    #service = TvTime(user)
    #service.sign_in()

    with open("src/html/home", 'r') as file:
            page = file.read()
    service = TvTimeParser()
    service.parse_links(page)

