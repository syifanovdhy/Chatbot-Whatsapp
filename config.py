import os

from dotenv import load_dotenv


load_dotenv()


NODE_URL = os.getenv(
    "NODE_URL",
    "http://127.0.0.1:3000"
)

APP_NAME = os.getenv(
    "APP_NAME",
    "STATARA"
)

APP_ENV = os.getenv(
    "APP_ENV",
    "development"
)