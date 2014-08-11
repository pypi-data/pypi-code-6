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

requirements = [line.strip() for line in open('requirements.txt')
                              .readlines()]

test_requirements = requirements.extend([
    'pytest',
    'mock'
])

setup(
    name='trellostats',
    version='0.9',
    description='Trello Stats for Winners',
    long_description=readme + '\n\n' + history,
    author='Ben Hughes',
    author_email='ben.hughes@actionagile.co.uk',
    url='https://github.com/actionagile/trellostats',
    packages=[
        'trellostats',
    ],
    package_dir={'trellostats':
                 'trellostats'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='Trello, Stats, Cycle Time, Reports, Burndown, Work In Progress, Kanban',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        # "Programming Language :: Python :: 2",
        # 'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts':
        ['trellostats=trellostats.cli:cli']
    }
)
