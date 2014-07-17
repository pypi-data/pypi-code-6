#!/usr/bin/env python
"""
LaunchKey-Flask
=========

:copyright: (c) 2014 by the 2013 LaunchKey, Inc.
:license: MIT, see LICENSE.txt for more details.
"""
import os

from setuptools import setup

module_path = os.path.join(os.path.dirname(__file__), 'flask_launchkey.py')
version_line = [line for line in open(module_path)
                if line.startswith('__version_info__')][0]

__version__ = '.'.join(eval(version_line.split('__version_info__ = ')[-1]))

setup(
    name='launchkey-flask',
    version=__version__,
    description='LaunchKey authentication extension for Flask',
    long_description=__doc__,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Brad Porter',
    url='https://github.com/LaunchKey/launchkey-flask',
    keywords='launchkey security authentication flask',
    license='MIT',
    py_modules=['flask_launchkey'],
    zip_safe=False,
    test_suite='tests',
    install_requires= [
        'launchkey-python',
        'flask',
        'flask-login',
    ],
    tests_require=[
        'mocker',
        'flask',
        'launchkey-python',
        'flask-login',
    ],
    )
