#!/usr/bin/env python

import os
import sys
from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='envar',
    version='0.1',
    description='Utility to load Environment Variables, minus the headache.',
    long_description=open('README.rst').read(),
    packages=['envar',],
    license='MIT',
    author='Harshad Sharma',
    author_email='harshad@sharma.io',
    url='https://www.github.com/hiway/envar/',
    test_suite='tests',
)
