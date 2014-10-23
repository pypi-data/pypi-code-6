#!/usr/bin/env python

from setuptools import setup


setup(
    name='http-cmd',
    version='0.1',
    url='https://github.com/lodevil/http-cmd',
    license='Apache License 2.0',
    author='lolynx',
    author_email='londevil@gmail.com',
    description='a library to simplify some simple'
                ' cmd interaction (http based)',
    packages=['httpcmd'],
    platforms='any',
    install_requires=[
        'flask>0.10',
        'requests>2.0',
    ],
    entry_points='''
        [console_scripts]
        httpcmd=httpcmd.cli:main
    '''
)
