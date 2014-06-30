from fabric.api import *


def start():
    local('python manage.py runserver')


def static():
    local('python manage.py collectstatic')


def sync():
    local('python manage.py syncdb')
