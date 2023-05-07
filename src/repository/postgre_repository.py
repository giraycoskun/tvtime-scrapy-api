from src.models.api import UserOut, UserDB


class PostgreSQLClient:
    def __init__(self, config):
        self.connection = None

    def get_user_out(self, username) -> UserOut:
        pass

    def get_user_db(self, username) -> UserDB:
        pass
