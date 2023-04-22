import logging
import os
from logging.handlers import TimedRotatingFileHandler

os.makedirs("logs", exist_ok=True)

log_formatter = logging.Formatter("%(asctime)s [%(levelname)-8s] %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)

file_handler = TimedRotatingFileHandler(
    "logs/log",
    when="midnight",
    backupCount=365,
    encoding="utf-8",
)
file_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def debug(msg):
    logger.debug(f"{msg}")


def info(msg):
    logger.info(f"{msg}")


def warn(msg):
    logger.warn(f"{msg}")


def error(msg):
    logger.error(f"{msg}")
