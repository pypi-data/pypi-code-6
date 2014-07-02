#!/usr/bin/env python
""" setup.py for goulash
"""
from setuptools import setup, find_packages
setup(
    name         = 'goulash',
    version      = '0.1',
    description  = 'toolbox, random shared stuff from my other projects',
    author       = 'mattvonrocketstein',
    author_email = '$author@gmail',
    url          = 'one of these days',
    download_url = 'https://github.com/mattvonrocketstein/goulash/tarball/0.1',
    package_dir  = {'': 'lib'},
    packages     = find_packages('lib'),
    keywords     = ['goulash'],
    )
