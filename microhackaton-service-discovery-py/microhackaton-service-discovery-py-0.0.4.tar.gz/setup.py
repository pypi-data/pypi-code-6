#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from setuptools import find_packages
from setuptools import setup

setup(
    name='microhackaton-service-discovery-py',
    version='0.0.4',
    description='A python package that works to provide service registration and discovery for http://microhackaton.github.io/2014/',
    author="Kamil Chmielewski",
    author_email='kamil.chm@gmail.com',
    url='https://github.com/microhackaton/service-discovery-py',
    license="ASL 2.0",
    install_requires=[
        'kazoo',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
    ],
    keywords="kazoo service discovery zookeeper",
    packages=find_packages(),
    long_description=open("README.rst", "r").read(),
)