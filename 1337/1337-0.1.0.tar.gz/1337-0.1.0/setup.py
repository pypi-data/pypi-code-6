#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
from setuptools import setup, find_packages

setup(
    name='1337',
    version='0.1.0',
    description='This is so 1337!',
    entry_points = {
        'console_scripts': [
            '1337 = 1337:main',
        ]
    }
)
