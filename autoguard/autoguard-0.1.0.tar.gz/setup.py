#!/usr/bin/env python
# Copyright (c) 2014 Polyconseil SAS
# This software is distributed under the two-clause BSD license.

from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='autoguard',
    version='0.1.0',

    description='Configuration setup for sentry',
    long_description=long_description,

    url='https://github.com/Polyconseil/autoguard',
    author="Polyconseil",
    author_email="opensource+autoguard@polyconseil.fr",
    license='BSD',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='sentry config',
    packages=find_packages(exclude=['venv', 'contrib', 'docs', 'tests*']),

    install_requires=[
        'sentry[postgres]==6.4.4',
        'getconf==1.0.1',
        'python-memcached==1.53',  # for cache
        'nydus==0.10.7',  # for buffers
    ],

    package_data={
        'autoguard': ['example_settings.ini'],
    },

    entry_points={
        'console_scripts': [
            'autoguard = autoguard.runner:main',
        ],
    },
)
