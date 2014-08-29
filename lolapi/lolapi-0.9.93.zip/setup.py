#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'lolapi',
    'lolapi.resources',
]

setup (
    name='lolapi',
    version='0.9.93',
    description='Python wrapper for the League of Legends RESTful API by Riot Games',
    author='Steven Motes',
    author_email='steven.motes@gmail.com',
    license='MIT',
    url='https://github.com/smotes/lolapi',
    packages=packages,
    py_modules=['lolapi'],
    platforms=['any'],
    requires='requests',
)