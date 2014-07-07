#!/usr/bin/env python
from setuptools import setup, find_packages

from txflask import version

setup(
    name="txflask",
    version=version,
    description="txflask makes working with Twisted Web as easy as working with flask",
    author="Brian Muller",
    author_email="bamuller@gmail.com",
    license="MIT",
    url="http://github.com/bmuller/txflask",
    packages=find_packages(),
    install_requires=['Twisted >= 12.1', 'routes >= 2.0']
)
