#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
]

setup(
    name='holmesalf',
    version='0.0.1',
    description='holmes-alf is a wrapper for OAuth 2 synchronous (based on alf) and asynchronous (based on the tornado-alf) clients that can bu used in holmes.',
    long_description='''
holmes-alf is a wrapper for OAuth 2 synchronous (based on alf) and asynchronous (based on the tornado-alf) clients that can bu used in holmes.
''',
    keywords='alf client client_credentials holmes oauth requests tornado',
    author='Globo.com',
    author_email='appdev@corp.globo.com',
    url='https://github.com/holmes-app/holmes-alf',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
    packages=find_packages(
        exclude=(
            'tests',
        ),
    ),
    include_package_data=True,
    install_requires=[
        'alf>=0.4.1',
        'tornado-alf>=0.3.1'
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
