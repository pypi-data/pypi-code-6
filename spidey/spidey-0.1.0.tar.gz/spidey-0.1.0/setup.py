#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='spidey',
    description='',
    version='0.1.0',
    author='A.J. May',
    url='',
    requires=[
        'requests(>=2.3.0)',
        'beautifulsoup4(>=4.3.2)',
    ],
    scripts=['bin/spidey'],
    license="MIT License",
    zip_safe = False,
)
