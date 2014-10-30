from datetime import datetime

__log = []
LOG_MAX = 1000
LOG_VIEW = 100


def _log(level, message, *args, **kwargs):
    print('[{:%y-%m-%d %H:%I:%S}] {:5.5}| {}'.format(datetime.now(), level, message.format(*args, **kwargs)))
    __log.append({
        'date': '{:%y-%m-%d %H:%I:%S}'.format(datetime.now()),
        'level': level,
        'message': message.format(*args, **kwargs),
    })

    if len(__log) > LOG_MAX:
        del __log[0]


def info(msg, *args, **kwargs):
    _log('info', msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    _log('error', msg, *args, **kwargs)


def log(msg, *args, **kwargs):
    _log('log', msg, *args, **kwargs)


def view(c):
    return {'type': 'log',
            'log': __log[-LOG_VIEW:], }
