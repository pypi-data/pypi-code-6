#!/usr/bin/env python
import os
from setuptools import setup

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as fh:
        return fh.read()

long_desciption_files = [ 'README.rst' ]
long_description = '\n\n'.join([read(f) for f in long_desciption_files])

setup(name='csputils',
    version='0.1.1',
    description='csputils - helpers for writing Content-Security-Policy rules',
    long_description=long_description,
    author='jbroadhead',
    author_email='jbroadhead@twitter.com',
    url='https://github.com/jamesbroadhead/csputils.git',
    packages = ['csputils'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

)
