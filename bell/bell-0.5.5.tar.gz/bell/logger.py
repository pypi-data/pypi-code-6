# coding=utf8

import logging
from logging import Formatter, getLogger, StreamHandler
import sys


# export
level_mappings = {
    5: logging.DEBUG,
    4: logging.INFO,
    3: logging.WARNING,
    2: logging.ERROR,
    1: logging.CRITICAL
}


logger = getLogger('Bell')
logger.setLevel(logging.DEBUG)

pattern = '%(name)s - %(levelname)s - %(asctime)s - %(message)s'
formatter = Formatter(pattern)

stdout_handler = StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
stdout_handler.setLevel(logging.DEBUG)
logger.addHandler(stdout_handler)


if __name__ == '__main__':
    message = 'test'
    logger.debug(message)
    logger.info(message)
    logger.warn(message)
    logger.error(message)
    logger.critical(message)
