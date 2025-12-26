import os, logging
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

def get_logging_function(level):
    if level == "debug":
        return logging.DEBUG
    elif level == "info":
        return logging.INFO
    elif level == "warning":
        return logging.WARNING
    elif level == "error":
        return logging.ERROR
    else:
        return logging.ERROR


class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PWD = os.getenv("DB_PWD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", 3306)

    LOG_LEVEL = get_logging_function(os.getenv("LOG_LEVEL"))
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PWD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    USE_SQLALCHEMY = int(os.getenv("USE_SQLALCHEMY", 0))
    SECRET_KEY = os.getenv("SECRET_KEY")

    SUPPORT_USER = os.getenv("SUPPORT_USER")
