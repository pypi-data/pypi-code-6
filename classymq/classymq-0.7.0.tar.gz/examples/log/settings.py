import logging
import os
from examples.log.handlers import AmqpLogger

logging.setLoggerClass(AmqpLogger)

USE_SLAVES = False

DATEFORMAT = '%d/%b/%Y %H:%M:%S'
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
HANDLER_LEVEL = LOG_LEVEL


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ' '.join(['%(hostname)8s | %(asctime)s', '%(levelname)8s', '- %(name)s',
                                '(%(funcName)s:%(lineno)d)', '\n\t%(message)s']),
            'datefmt': DATEFORMAT,
            },
        'default': {
            'format': ' '.join(['%(hostname)8s | %(asctime)s', '%(levelname)8s', '- %(message)s']),
            'datefmt': DATEFORMAT,
            },
        },
    'handlers': {
        'console_handler': {
            'level': HANDLER_LEVEL,
            'formatter':'verbose',
            'class': 'logging.StreamHandler',
            },
    },
    'loggers': {
        '': {
            'handlers':['console_handler', 'rotating_handler'],
            'propagate': True,
            'level': LOG_LEVEL,
            },
        }
}
