import log_watcher
import imp
import logging.config

# -----------------------------------------------------------------------------

PATH_TO_SETTINGS = '/opt/log_watcher/settings.py'

# -----------------------------------------------------------------------------
# Set app settings to log_watcher.settings endpoint

if not hasattr(log_watcher, 'settings'):
    log_watcher.settings = imp.load_source(
        'log_watcher.settings',
        PATH_TO_SETTINGS)

# -----------------------------------------------------------------------------
# Configure logging

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
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    },
}

# Handle sentry conf
from log_watcher import settings
if hasattr(settings, 'SENTRY_DSN'):
    LOGGING['handlers']['sentry'] = {
        'level':'ERROR',
        'class':'raven.handlers.logging.SentryHandler',
        'dsn': settings.SENTRY_DSN,
    }
    LOGGING['loggers']['']['handlers'].append('sentry')

logging.config.dictConfig(LOGGING)
