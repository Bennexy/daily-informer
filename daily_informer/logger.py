import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from os import getenv as env
from os import environ

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = "daily-informer.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight", interval=1)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, add_log_file=True):
    logger = logging.getLogger(logger_name)
    logger.setLevel(get_logger_level())
    # logger.setLevel(logging.INFO)
    #logger.setLevel(logging.DEBUG)
    
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True
    if print_log_to_console():
        logger.addHandler(get_console_handler())
    if add_log_file:
        logger.addHandler(get_file_handler())
    logger.propagate = True
    return logger


def get_logger_level():
    key = env("LOG_LEVEL")
    if key in environ:
        if key in ("CRITICAL", "FATAL"):
            return logging.CRITICAL
        if key in ("ERROR"):
            return logging.ERROR
        if key in ("WARNING", "FATAL"):
            return logging.WARNING
        if key in ("INFO"):
            return logging.INFO
        if key in ("DEBUG"):
            return logging.DEBUG
        return logging.ERROR
    return logging.ERROR


def print_log_to_console():
    key =env("LOG_TO_CONSOLE")
    if key in environ:
        if key.upper() in ("TRUE"):
            return True
        try:
            res = int(environ.get(key))
            if res == 1:
                return True
        except ValueError:
            return False
    return False