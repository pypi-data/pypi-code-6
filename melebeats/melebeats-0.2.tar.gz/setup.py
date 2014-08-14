#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from mele import __version__



setup(
    name='melebeats',
    version=__version__,
    description='for the lolz',
    author='Kim Thoenen',
    author_email='kim@smuzey.ch',
    url='https://github.com/Chive/melebeats',
    packages=find_packages(),
    license='MIT',
    platforms=['OS Independent'],
    classifiers=None,
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'mele = mele:beat',
        ]
    },
    install_requires=[
        'termcolor',
    ],
)