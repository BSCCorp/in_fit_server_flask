import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    TESTING = False
    JSON_SORT_KEYS = False
