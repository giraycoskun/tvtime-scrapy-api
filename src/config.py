import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")

REDIS_URL = os.getenv("REDIS_URL")
