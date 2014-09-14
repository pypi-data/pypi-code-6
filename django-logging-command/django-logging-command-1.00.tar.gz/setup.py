#!/usr/bin/env python
from distutils.core import setup

readme = open('README.rst').read()

setup(
    name='django-logging-command',
    version='1.00',
    author_email='gattster@gmail.com',
    author='Philip Gatt',
    description="A mixin to make custom Django management commands set the logger to "
                "an appropriate level",
    long_description=readme,
    url='http://github.com/defcube/django-logging-command/',
    py_modules=["django_logging_command"],
    data_files=[('', ['README.rst'])],
    )