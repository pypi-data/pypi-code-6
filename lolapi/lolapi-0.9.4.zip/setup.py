#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import lolapi

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist register upload')
    sys.exit()

packages = [
    'lolapi',
]

with open('requirements.txt') as f:
    requires = f.read().split('\n')

setup(
    name=lolapi.__name__,
    version=lolapi.__version__,
    #packages=['lolapi', 'lolapi.resources'],
    url=lolapi.__url__,
    license=lolapi.__license__,
    author=lolapi.__author__,
    author_email='steven.motes@gmail.com',
    description='a Python wrapper for League of Legends RESTful API by Riot Games',
    packages=packages,
    package_dir={'lolapi': 'lolapi'},
    include_package_data=True,
    install_requires=requires,
)
