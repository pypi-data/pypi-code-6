#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

version = "0.0.1"

setup(
    name="randua",
    version=version,
    description="Random User Agent string generator",
    author="Naglis Jonaitis",
    author_email="njonaitis@gmail.com",
    keywords=["browser", "useragent"],
    url="https://github.com/naglis/randua",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: Public Domain",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    py_modules=["randua"],
    entry_points={"console_scripts": [ "randua = randua:main" ]},
)
