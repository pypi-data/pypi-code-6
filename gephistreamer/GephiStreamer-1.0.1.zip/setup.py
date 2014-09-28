#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import GephiStreamer

setup(

    name='GephiStreamer',

    version=GephiStreamer.__version__,

    packages=find_packages(),

    author="@totetmatt",

    author_email="matthieu.totet@gmail.com",

    description="Tools to stream data to gephi",

    long_description=open('README.md').read(),

    install_requires=['requests'] ,

    include_package_data=True,
    
    url='http://github.com/totetmatt/GephiStreamer',
    
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Communications",
    ],
    
    entry_points = {},
    
    license="WTFPL",

)