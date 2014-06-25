#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python libmbfl bindings setup file"""

from distutils.core import setup

setup(
    name="pymbfl",
    version="0.2",
    author="Dmitry Selyutin",
    author_email="ghostmansd@solidlab.ru",
    packages=["pymbfl"],
    url="http://pypi.python.org/pypi/pymbfl/",
    license="LICENSE.txt",
    description="Python libmbfl bindings",
    long_description=open("README.txt").read(),
)
