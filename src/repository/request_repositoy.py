from requests import Session
from loguru import logger

from src.models.api import TVTimeUser
from src.config import (
    TVTIME_URL,
    TVTIME_SIGNIN_URL,
    TVTIME_SIGNOUT_URL,
    TVTIME_TOWATCH_URL,
    TVTIME_HOST,
    USER_AGENT,
)


class TVTimeClient:
    def __init__(self, user: TVTimeUser) -> None:
        self.user = user
        self.session = Session()
        headers = {"User-Agent": USER_AGENT, "Host": TVTIME_HOST}
        self.session.headers.update(headers)

    def login(self):
        payload = {
            "username": self.user.username,
            "password": self.user.password,
            "redirect_path": TVTIME_TOWATCH_URL,
        }
        self.session.post(TVTIME_SIGNIN_URL, data=payload)

    def show_seasons(self, show_id):
        url = f"{TVTIME_URL}show_seasons?show_id={show_id}"
        response = self.session.get(url)
        logger.debug("Show Seasons: {response}", response=response.status_code)
        logger.debug("Show Seasons: {response}", response=response.text)
        return response

    def mark_show_followed(self, show_id, follow=True):
        url = f"{TVTIME_URL}followed_shows"
        data = {"show_id": show_id}
        if follow:
            response = self.session.put(url=url, data=data)
        else:
            response = self.session.delete(url=url, data=data)
        logger.debug("Follow Show: {response}", response=response.status_code)
        logger.debug("Follow Show: {response}", response=response.text)
        return response

    def mark_season_watched(self, show_id, season, watched=True):
        url = f"{TVTIME_URL}watched_season"
        data = {"show_id": show_id, "season": season}
        if watched:
            response = self.session.put(url=url, data=data)
        else:
            response = self.session.delete(url=url, data=data)
        logger.debug("Watched Season: {response}", response=response.status_code)
        logger.debug("Watched Season: {response}", response=response.text)

    def mark_episode_watched(self, episode_id, watched=True):
        url = f"{TVTIME_URL}watched_episodes"
        data = {"episode_id": episode_id}
        if watched:
            response = self.session.put(url=url, data=data)
        else:
            response = self.session.delete(url=url, data=data)
        logger.debug("Watched Episode: {response}", response=response.status_code)
        logger.debug("Watched Episode: {response}", response=response.text)

    def mark_show_until_watched(self, season, episode, show_id):
        url = f"{TVTIME_URL}show_watch_until"
        data = {"season": season, "episode": episode, "show_id": show_id}
        response = self.session.put(url=url, data=data)
        logger.debug("Watched Until: {response}", response=response.status_code)
        logger.debug("Watched Until: {response}", response=response.text)

    def get_show_ratings(self, show_id):
        url = f"{TVTIME_URL}show/{show_id}/ratings"
        response = self.session.get(url)
        logger.debug("Show Ratings: {response}", response=response.status_code)
        logger.debug("Show Ratings: {response}", response=response.text)
        return response

    def logout(self):
        logger.debug("Logout TVTimeClient")
        self.session.get(TVTIME_SIGNOUT_URL)
        self.session.close()


if __name__ == "__main__":
    pass
    # user = TVTimeUser(username=TVTIME_TEST_USERNAME, password=TVTIME_TEST_PASSWORD)
    # tv_time_client = TVTimeClient(user)
    # tv_time_client.login()
    # tv_time_client.get_show_ratings(394290)
    # tv_time_client.mark_episode_watched(8112670, watched=False)
    # tv_time_client.show_seasons(394290)
    # tv_time_client.logout()
