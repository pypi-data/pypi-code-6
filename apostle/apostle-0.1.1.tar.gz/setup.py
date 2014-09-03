#!/usr/bin/env python

import os
import sys

import apostle

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'apostle'
]

requires = [
	'requests'
]
tests_require=[
	'mock'
]

setup(
    name=apostle.__title__,
    version=apostle.__version__,
    description='Python Bindings for Apostle.io',
    long_description='Python Bindings for Apostle.io',
    author='Mal Curtis',
    author_email='mal@apostle.io',
    url='http://apostle.io',
    packages=packages,
	tests_require=tests_require,
	test_suite='apostle.tests',
    install_requires=requires,
    license='MIT',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',

    ),
)
