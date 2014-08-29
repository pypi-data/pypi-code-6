#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from distutils.core import setup

import lolapi

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('README.rst') as f:
    readme = f.read()
with open('requirements.txt') as f:
    requires = f.read().split('\n')

setup (
    name=lolapi.__name__,
    version=lolapi.__version__,
    description='Python wrapper for the League of Legends RESTful API by Riot Games',
    author=lolapi.__author__,
    author_email='steven.motes@gmail.com',
    license=lolapi.__license__,
    url='https://github.com/smotes/lolapi',
    py_modules=['lolapi'],
    platforms=['any'],
    requires='requests',
)