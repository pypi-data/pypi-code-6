#!/usr/bin/env python

import os

try:
    from setuptools import setup, Extension, Command
except ImportError:
    from distutils.core import setup, Extension, Command

import spliterator

setup(
    name='spliterator',
    version=spliterator.__version__,
    description=spliterator.__description__,
    long_description=open('README.rst').read(),
    author=spliterator.__author__,
    author_email=spliterator.__author_email__,
    url=spliterator.__url__,
    license=spliterator.__license__,
    packages=['spliterator'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
