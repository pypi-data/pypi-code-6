#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-url-redirect',
    version='0.1.0',
    description='Simple redirect middleware for Django',
    author='Gizmag',
    author_email='tech@gizmag.com',
    url='https://github.com/gizmag/django-url-redirect/',
    packages=find_packages(exclude=['tests']),
    install_requires=['django>=1.5']
)
