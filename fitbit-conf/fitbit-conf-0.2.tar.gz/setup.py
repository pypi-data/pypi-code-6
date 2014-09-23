#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.version_info < (3,):
    print('Please, install and use python3.\nInstallation is aborted.')
    exit(1)

try:
    from setuptools import setup, find_packages
except ImportError:
    import distribute_setup

    distribute_setup.use_setuptools()
    from setuptools import setup

with open('README.txt') as file:
    long_description = file.read()

setup(
    name='fitbit-conf',
    version='0.2',
    description='fitbit configuration tasks',
    long_description=long_description,
    author='Igor Kuplevich',
    author_email='ikuplevich@fitbit.com',
    url='www.fitbit.com',
    platforms='any',
    keywords=['fitbit', 'configuration'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fitbit-ch = conf.ch:main',
            'fitbit-dbup = conf.dbupdate:main'
        ],
    }
)