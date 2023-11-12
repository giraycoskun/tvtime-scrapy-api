"""Configure Project

    ENVIRONMENT: development, production
    REDIS
    POSTGRES
    TVTIME
    JWT
"""
import os
from base64 import b64encode
from secrets import token_bytes

from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
TVTIME_TEST_USERNAME = os.getenv("TVTIME_TEST_USERNAME")
TVTIME_TEST_PASSWORD = os.getenv("TVTIME_TEST_PASSWORD")

REDIS_URL = os.getenv("REDIS_URL")
REDIS_CACHE_URL = os.getenv("REDIS_CACHE_URL")

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
TVTIME_HOST = "www.tvtime.com"
TVTIME_URL = "https://www.tvtime.com/"
TVTIME_SIGNIN_URL = "https://www.tvtime.com/signin"
TVTIME_SIGNOUT_URL = "https://www.tvtime.com/signout"
TVTIME_TOWATCH_URL = "https://www.tvtime.com/en/to-watch"
TVTIME_UPCOMING_URL = "https://www.tvtime.com/en/upcoming"
TVTIME_PROFILE_URL = "https://www.tvtime.com/en/user/"

TVTIME_TEST_USERNAME = os.getenv("TVTIME_TEST_USERNAME")
TVTIME_TEST_PASSWORD = os.getenv("TVTIME_TEST_PASSWORD")

JWT_SECRET_KEY = b64encode(token_bytes(32)).decode()
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30