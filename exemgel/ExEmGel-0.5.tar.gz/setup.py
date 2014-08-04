#! /usr/bin/env python
from __future__ import with_statement
import sys
import os
from setuptools import setup

with open('README.rst') as file:
    long_description = file.read()

if sys.argv[-1] == 'publish':                                                                                    
    os.system('python setup.py sdist upload')                                                                    
    sys.exit() 

setup(
    name='ExEmGel',
    version='0.5',
    author = "Dave Collins",
    author_email = "dave@hopest.net",
    packages=['exemgel',],
    license='MIT',
    description = "Simple xml reader",
    url = "https://github.com/thedavecollins/ExEmGel",
    long_description=long_description,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    "License :: OSI Approved",
    "License :: OSI Approved :: MIT License",

    "Topic :: Text Processing",
    "Topic :: Text Processing :: Markup",
    "Topic :: Text Processing :: Markup :: XML",

    ],
)
