#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lurkmoar import __version__
from setuptools import setup

setup(
    name='lurkmoar',
    version=__version__,
    author='Louis Thibault',
    author_email='louist87@gmail.com',
    packages=['lurkmoar'],
    include_package_data=True,
    install_requires=['requests'],
    url='',
    license='Unlicense',
    description='4chan API wrapper geared towards text analysis',
    keywords=['4chan', 'b', '/b/', 'imageboard', 'bbs', 'text'],
    long_description=''
)
