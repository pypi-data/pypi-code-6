import logging


def format_string():
    return logging.Formatter('[%(levelname)s] %(name)s '
                             '%(lineno)d: %(message)s')
