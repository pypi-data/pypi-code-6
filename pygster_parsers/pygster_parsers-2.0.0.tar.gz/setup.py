#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup for pygster_parsers.

Source:: https://github.com/OnBeep/pygster_parsers
"""

__title__ = 'pygster_parsers'
__version__ = '2.0.0'
__author__ = 'Greg Albrecht  <gba@onbeep.com>'
__copyright__ = 'Copyright 2014 OnBeep, Inc. and Contributors'
__license__ = 'Apache License, Version 2.0'


import os
import sys


try:
    from setuptools import setup
except ImportError:
    # pylint: disable=F0401,E0611
    from distutils.core import setup


def publish():
    """Function for publishing package to pypi."""
    if sys.argv[-1] == 'publish':
        os.system('python setup.py sdist upload')
        sys.exit()


publish()


setup(
    name=__title__,
    version=__version__,
    description='Pygster Parsers',
    long_description=open('README.rst').read(),
    author='Greg Albrecht',
    author_email='gba@onbeep.com',
    license=open('LICENSE').read(),
    url='https://github.com/OnBeep/pygster_parsers',
    setup_requires=['nose'],
    tests_require=['coverage', 'nose'],
    install_requires=['pygster'],
    package_dir={'pygster_parsers': 'pygster_parsers'},
    packages=['pygster_parsers'],
    zip_safe=False
)
