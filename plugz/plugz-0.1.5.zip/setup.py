#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools.command.test import test as TestCommand

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import plugz

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
]

setup(
    name='plugz',
    version= plugz.__version__,
    description='Plugin framework that simplifies plugin support in your tools',
    long_description=readme + '\n\n' + history,
    author='Matti Gruener',
    author_email='matti@mistermatti.com',
    url='https://github.com/mistermatti/plugz',
    packages=[
        'plugz',
        'plugz.errors',
        'plugz.plugintypes'
    ],
    package_dir={'plugz':
                 'plugz'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='plugz',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
