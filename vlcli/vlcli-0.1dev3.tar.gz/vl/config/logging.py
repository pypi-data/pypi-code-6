import os.path

log_dir = os.path.join(os.path.expanduser('~'), '.vl/logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir, mode=0700)


def get_config(debug=False):
    config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(name)s %(lineno)-4d %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'verbose',
                'filename': os.path.join(log_dir, 'vlcli.log'),
                'maxBytes': 10485760,
                'backupCount': 3
            }
        },
        'loggers': {
            'vl': {
                'handlers': ['file'],
                'level': 'WARNING',
            }
        }
    }

    if debug:
        config['loggers']['vl']['level'] = 'DEBUG'
    return config
