#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import version_info

from setuptools import setup

assert version_info >= (2, 6)
requirements = ['PyRSS2Gen']
if version_info < (2, 7):
    requirements.append('argparse')

setup(
    name='rtorrent-notify',
    version='1.1.0',
    description='Notify of rtorrent events, through RSS or IRC (using Irker)',
    long_description=open('README').read(),
    author='Laurent Bachelier',
    author_email='laurent@bachelier.name',
    url='http://git.p.engu.in/laurentb/rtorrent-notify/',
    packages=['rtorrentnotify'],
    install_requires=requirements,
    test_suite='rtorrentnotify.test',
    tests_require='nose>=1.0',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
    ],
    entry_points={'console_scripts': ['rtorrent-notify = rtorrentnotify.__main__:main']},
)
