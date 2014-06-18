import logging
import logging.config

class Settings:
    def __init__(self, data={}):
        self.__dict__.update(data)


class RequestSettings(Settings):
    HEADERS = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
        "accept": "text/html",
        'content-type': "application/x-www-form-urlencoded"
    }
    AUTOTHROTTLE = False
    CACHE = None
    TIMEOUT = 5
    DELAY = 0.5
    MIN_DELAY = 0.5
    MAX_DELAY = 60


class LogSettings:
    version = 1
    disable_existing_loggers = True
    formatters = {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    }
    handlers = {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    }
    loggers = {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'dragline': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        }
    }

    def __init__(self, formatters={}, handlers={}, loggers={}):
        self.formatters.update(formatters)
        self.handlers.update(handlers)
        self.loggers.update(loggers)

    def getLogger(self, name=None):
        attrs = ['version', 'disable_existing_loggers', 'handlers', 'loggers',
                 'formatters']
        conf = {attr: getattr(self, attr) for attr in attrs}
        logging.config.dictConfig(conf)
        return logging.getLogger(name=name)


class CrawlSettings(Settings):
    MODE = "NORM"
    MAX_RETRY = 3
    REDIS_URL = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 1


class SpiderSettings(Settings):
    pass
