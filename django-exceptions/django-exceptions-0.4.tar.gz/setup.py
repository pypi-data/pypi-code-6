#!/usr/bin/env python

from setuptools import (
    setup,
)

setup(
    name='django-exceptions',
    version='0.4',
    author='aRkadeFR',
    author_email='contact@arkade.info',
    url='https://github.com/aRkadeFR/django-exceptions',
    download_url='https://github.com/aRkadeFR/django-exceptions/tarball/v0.4',
    description='Django app to handle exceptions in a comfortable way',
    packages=['django_exceptions'],
    package_dir={'': 'project'},
    classifiers=[
        'Framework :: Django',
    ],
)
