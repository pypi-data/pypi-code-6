import os

from djangomaster.urls import urlpatterns


def get_version():
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, 'version.txt')
    return open(path).read().strip()

__version__ = get_version()


def get_urls():
    return urlpatterns, 'djangomaster', 'djangomaster'

urls = get_urls()
