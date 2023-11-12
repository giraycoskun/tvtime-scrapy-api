from abc import ABC, abstractmethod


class TVService(ABC):

    @abstractmethod
    def get_watching_shows():
        raise NotImplementedError

    @abstractmethod
    def get_upcoming_shows():
        raise NotImplementedError