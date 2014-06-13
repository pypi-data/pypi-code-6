class Settings:
    def __init__(self, data={}):
        self.__dict__.update(data)

    LOGCONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
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
    }


class RequestSettings(Settings):
    HEADERS = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
        "accept": "text/html",
        'content-type': "application/x-www-form-urlencoded"
    }
    CACHE = None
    DELAY = 0.5
    MIN_DELAY = 0.5
    MAX_DELAY = 60


class CrawlSettings(Settings):
    MODE = "NORM"
    MAX_RETRY = 3
    REDIS_URL = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 1


class SpiderSettings(Settings):
    pass
