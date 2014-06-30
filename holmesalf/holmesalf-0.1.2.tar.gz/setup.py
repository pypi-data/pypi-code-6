#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of holmesalf.
# https://github.com/holmes-app/holmes-alf

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Pablo Aguiar scorphus@gmail.com


from setuptools import setup, find_packages
from holmesalf import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='holmesalf',
    version=__version__,
    description='holmes-alf is a wrapper for OAuth 2 synchronous (based on alf) and asynchronous (based on the tornado-alf) clients that can bu used in holmes.',
    long_description='''
holmes-alf is a wrapper for OAuth 2 synchronous (based on alf) and asynchronous (based on the tornado-alf) clients that can bu used in holmes.
''',
    keywords='alf client client_credentials holmes oauth requests tornado',
    author='Pablo Aguiar',
    author_email='scorphus@gmail.com',
    url='https://github.com/holmes-app/holmes-alf',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'alf>=0.4.1',
        'tornado-alf>=0.3.3'
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'holmesalf=holmesalf.cli:main',
        ],
    },
)
