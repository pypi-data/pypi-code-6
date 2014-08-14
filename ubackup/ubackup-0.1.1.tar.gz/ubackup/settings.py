import os

DEFAULT_SETTINGS_PATH = '/opt/ubackup/settings.py'

CHUNK_SIZE = 1024 * 1024 * 10

CURRENT_DIR = os.path.dirname(__file__)
VERSION = open(os.path.join(CURRENT_DIR, 'VERSION.txt')).read()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # this fixes the problem

    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'requests': {
            'level': 'WARNING',
            'handlers': ['console'],
        }
    },
}

DROPBOX_APP_KEY = 'rqqumcq9htn0fcb'
DROPBOX_APP_SECRET = 'ag8dvti5kx2cfg9'

# Handle sentry conf
# if hasattr(settings, 'SENTRY_DSN'):
#     settings.LOGGING['handlers']['sentry'] = {
#         'level': 'ERROR',
#         'class': 'raven.handlers.logging.SentryHandler',
#         'dsn': settings.SENTRY_DSN,
#     }
#     settings.LOGGING['loggers']['']['handlers'].append('sentry')
