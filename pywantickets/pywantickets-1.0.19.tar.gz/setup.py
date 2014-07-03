#!/usr/bin/env python

import os
import sys

import pywantickets

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'pywantickets'
]

requires = ['requests']

setup(
    name='pywantickets',
    version=pywantickets.__version__,
    description='Wantickets.com implementation for Python.',
    long_description=open('README.txt').read(),
    author='Gamaliel Espinoza',
    author_email='gespinoza@edesarrollos.com',
    url='http://bitbucket.org/edesarrollos/pywantickets',
    packages=packages,
    package_data={'': ['LICENSE', 'NOTICE'], 'pywantickets': ['*.pem']},
    package_dir={'pywantickets': 'pywantickets'},
    include_package_data=True,
    install_requires=requires,
    # license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',

    ),
)
