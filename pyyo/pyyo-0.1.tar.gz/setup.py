#/usr/bin/env python
#coding:utf8

from setuptools import setup, find_packages

setup(
    name = 'pyyo',
    version = '0.1',
    keywords = ('yo'),
    description = 'Send yo using python',
    license = 'GPL v2',
    install_requires =['python>=2.5'],

    author = 'fangh',
    author_email = 'gavintofan@gmail.com',

    packages = find_packages(),
    platforms = 'any',
    )
