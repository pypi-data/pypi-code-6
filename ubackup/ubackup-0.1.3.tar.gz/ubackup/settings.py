import os

DEFAULT_SETTINGS_PATH = '/opt/ubackup/settings.py'

CHUNK_SIZE = 1024 * 1024 * 10

CURRENT_DIR = os.path.dirname(__file__)
VERSION = open(os.path.join(CURRENT_DIR, 'VERSION.txt')).read()

DROPBOX_APP_KEY = 'rqqumcq9htn0fcb'
DROPBOX_APP_SECRET = 'ag8dvti5kx2cfg9'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

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

# Add a RotatingFileHandler to logging
if not os.environ.get('TESTING'):
    if not os.path.exists('/var/log/ubackup'):
        try:
            os.mkdir('/var/log/ubackup')
        except OSError:
            pass
    if os.path.exists('/var/log/ubackup'):
        LOGGING['handlers']['rotate_file'] = {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': '/var/log/ubackup/ubackup.log',
            'backupCount': 5,
            'maxBytes': 1024 * 1024 * 20
        }
        for logger, obj in LOGGING['loggers'].items():
            obj['handlers'].append('rotate_file')
