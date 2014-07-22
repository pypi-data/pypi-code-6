#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'rsj217'

from setuptools import setup, find_packages

setup(
    name='xiami',
    version='0.0.1',
    keywords = ('xiami', 'music', 'download'),
    description='This is a xiami music download clinet',
    license = 'MIT License',
    author='rsj217',
    author_email='rsj217@gmail.com',
    url='https://rsj217.github.io/',
    packages=find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
)