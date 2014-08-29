#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from distutils.core import setup

import lolapi

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup (
    name='lolapi',
    version='0.9.9',
    description='Python wrapper for the League of Legends RESTful API by Riot Games',
    author='Steven Motes',
    author_email='steven.motes@gmail.com',
    license='MIT',
    url='https://github.com/smotes/lolapi',
    py_modules=['lolapi'],
    platforms=['any'],
    requires='requests',
)