#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    "bsddb3>=5.2.0"
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='federated_monsters',
    version='0.3.0',
    description='Federated Monsters is a game that seeks to follow the format of games like Pokemon, but to instead use a federated server format to store and trade creatures',
    long_description=readme + '\n\n' + history,
    author='Colin Atkinson',
    author_email='colin.william.atkinson@gmail.com',
    url='https://github.com/colatkinson/federated_monsters',
    packages=[
        'federated_monsters',
    ],
    package_dir={'federated_monsters':
                 'federated_monsters'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='federated_monsters',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    #tests_require=test_requirements
    tests_require=requirements
)
