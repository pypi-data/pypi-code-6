import logging


def ml(logger=None, file_path=None, log_level=None):

    if not logger:
        logger = "mylogger"

    if not log_level:
        log_level = logging.DEBUG

    if not file_path:
        file_path = '/var/log/mylogger/{}.log'.format(logger)

    ml = logging.getLogger(logger)
    ml.setLevel(log_level)
    handler = logging.FileHandler(file_path)
    format = "%(created)s %(module)s %(funcName)s %(lineno)d %(message)s"
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    ml.addHandler(handler)

    return ml
