#!/usr/bin/env python
from distutils.core import setup
from asyncore_patch import __version__ as version

setup(
    name='asyncore_patch',
    version=version,
    packages=[''],
    url='https://github.com/shuge/asyncore_patch',
    license='MIT License',
    author='Shuge Lee',
    author_email='shuge.lee@gmail.com',
    description='epoll patch for asyncore',

    platforms = ["Linux"],
    py_modules=['asyncore_patch'],
)
