#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup, find_packages

MODULE_NAME = 'flask_cache_external_assets'
DEPENDENCIES = [
    'flask',
    'python-magic >=0.4',
]
TEST_DEPENDENCIES = []

metadata_relpath = '{}/metadata.py'.format(MODULE_NAME)

# Get package metadata. We use exec here instead of importing the
# package directly, so we can avoid any potential import errors.
with open(metadata_relpath) as fh:
    metadata = {}
    exec(fh.read(), globals(), metadata)


setup(
    name=MODULE_NAME,
    version=metadata['__version__'],
    description='Flask extension for caching external assets',
    long_description='Long Grenier',
    author='CALC',
    author_email='contact@camembertaulaitcrew.biz',
    url='http://camembertaulaitcrew.biz',
    packages=find_packages(),
    install_requires=DEPENDENCIES,
    tests_require=DEPENDENCIES + TEST_DEPENDENCIES,
    dependency_links=[
    ],
    test_suite=MODULE_NAME + '.tests',
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='MIT',
    extras_require={
        'shell': ['ipython >=1.1.0'],
        'tests': TEST_DEPENDENCIES,
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
