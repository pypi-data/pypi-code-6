#!/usr/bin/env python

import os
import sys

from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import csvcleaner

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name=csvcleaner.__title__,
    version=csvcleaner.__version__,
    description=csvcleaner.__description__,
    long_description=readme,
    author=csvcleaner.__author__,
    author_email=csvcleaner.__email__,
    url=csvcleaner.__url__,
    packages=['csvcleaner'],
    package_data={'': ['LICENSE']},
    package_dir={'csvcleaner': 'csvcleaner'},
    include_package_data=True,
    install_requires=[],
    license=csvcleaner.__license__,
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    )
)
