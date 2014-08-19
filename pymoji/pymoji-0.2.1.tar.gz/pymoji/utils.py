# -*- encoding: utf-8 -*-

from pkg_resources import get_distribution, DistributionNotFound


class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def ensure_unicode(text):
    if isinstance(text, unicode):
        return text
    return text.decode('utf-8')


def get_package_version():
    try:
        _dist = get_distribution('pymoji')
    except DistributionNotFound:
        __version__ = 'Please install this project with setup.py'
    else:
        __version__ = _dist.version
    return __version__
