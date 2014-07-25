import os
from setuptools import setup

import django_websocket

setup(
    name = "django-gevent-websocket",
    version = django_websocket.__version__,
    description = "Easy WebSocket server for django using gevent-websocket",
    long_description = open("README.rst").read(),
    url = "http://bitbucket.org/schinckel/django-gevent-websocket/",
    author = "Matthew Schinckel",
    author_email = "matt@schinckel.net",
    packages = [
        "django_websocket",
    ],
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    test_suite='tests.main',
    install_requires=[
        'gevent',
        'gevent-websocket',
        'django',
    ]
)
