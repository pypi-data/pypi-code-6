#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='spidey',
    description='',
    version='0.1.1',
    author='A.J. May',
    url='',
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    scripts=['bin/spidey'],
    license="MIT License",
    zip_safe=False,
)
