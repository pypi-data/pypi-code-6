#!/usr/bin/env python

import os
import sys

sys.path.append(os.getcwd() + "/src/")

import restler

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

f = open('README.md', 'r')
readme = f.read()
f.close()

tags = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
]

setup(
    name="librestler",
    version=restler.__version__,
    description="Object Oriented rest client",
    long_description=readme,
    license="Apache 2.0",

    author="Jeff Ostendorf",
    author_email="jostendorf@gmail.com",
    url="http://jdost.us/restler/",

    packages=['restler'],
    package_dir={'restler': 'src/restler'},
    package_data={'': ["LICENSE"]},
    include_package_data=True,

    classifiers=tags
)
