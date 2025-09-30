import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logger(name=__name__, log_file='app.log', level=logging.INFO):
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')

    handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()
