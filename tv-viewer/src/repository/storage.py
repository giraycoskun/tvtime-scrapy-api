from abc import ABC, abstractmethod
from uuid import UUID

from .schema import User

class Storage(ABC):

    @abstractmethod
    def get_user(id: UUID):
        raise NotImplementedError

    @abstractmethod
    def set_user(user:User):
        raise NotImplementedError
