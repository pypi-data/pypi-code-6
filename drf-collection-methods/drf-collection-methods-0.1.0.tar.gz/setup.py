#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='drf-collection-methods',
    version='0.1.0',
    description='Route methods to the base of your collections!',
    author='Gizmag',
    author_email='tech@gizmag.com',
    url='https://github.com/gizmag/drf-collection-methods',
    packages=find_packages(),
    install_requires=['django', 'djangorestframework']
)
