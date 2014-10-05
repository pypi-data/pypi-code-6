#!/usr/bin/env python

from setuptools import (
    setup,
)

setup(
    name='django-exceptions',
    version='0.3',
    author='aRkadeFR',
    author_email='contact@arkade.info',
    url='http://arkadefr.github.io/',
    description='Django app to handle exceptions in a comfortable way',
    packages=['django_exceptions'],
    package_dir={'': 'project'},
    classifiers=[
        'Framework :: Django',
    ],
)
