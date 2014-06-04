#!/bin/env python3
# -*- coding: utf-8 -*-
"""
Greyskull in deployment is configured using environment variables, installing this package and
configuring it via your preferred web server is recommended.
"""

from setuptools import setup

setup(
    name="Greyskull",
    version="0.0.1.dev1",
    description="A lightweight, bittorrent-compatible, NTrack tracker",
    long_description=open("README.rst", 'rb').read().decode('utf-8'),
    url='http://github.com/xj9/greyskull',
    license="MIT/ISC",
    author="Carlos Killpack",
    author_email="carlos.killpack@rocketmail.com",
    packages=[
        'greyskull',
    ],
    install_requires=[
        'tornado',
        'python3-memcached',
    ],
    classifiers=[
        'License :: Public Domain',
        'License :: OSI Approved',
        'License :: OSI Approved :: ISC License (ISCL)',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Networking',
    ]
)
