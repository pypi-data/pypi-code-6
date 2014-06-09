#!/usr/bin/env python
# vim: set fileencoding=utf-8 nofoldenable:

from setuptools import setup
from setuptools.command.install import install
from distutils.command.install_data import install_data
from glob import glob
from grp import getgrnam
from pwd import getpwnam
import os
import subprocess
import sys


def glob_files(pattern):
    return [f for f in glob(pattern) if os.path.isfile(f)]

# Files to install:
data_files = [
    #('share/ardj/database', glob_files('share/database/*.sql')),
    ('share/ardj/failure', ['share/audio/stefano_mocini_leaving_you_failure_edit.ogg']),
    ('share/ardj/samples', ['share/audio/cubic_undead.mp3', 'share/audio/successful_install.ogg']),
    ('share/ardj/shell-extensions/zsh', ['share/shell-extensions/zsh/_ardj']),
    ('share/doc/ardj', ('NEWS', 'README.txt', 'TODO')),
    ('share/doc/ardj/examples', glob_files('share/doc/examples/*')),
    ('share/doc/ardj/html/', glob_files('share/doc/html/*')),
    ('share/man/man1', ['share/doc/man/ardj.1']),
    ('lib/ardj', ['bin/ardj-next-track', 'bin/ezstream-meta']),
]

classifiers = [
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: Unix',
    'Programming Language :: Python',
    'Topic :: Internet',
    ]


setup(
    author = 'Justin Forest',
    author_email = 'hex@umonkey.net',
    classifiers = classifiers,
    data_files = data_files,
    description = 'An artificial DJ for you internet radio.',
    long_description = 'An artificial DJ for your icecast2 based internet radio.  Consists of an ezstream python playlist module, a jabber bot which lets you control that radio, integrates with Last.fm and Twitter, can download music from Jamendo, etc.',
    license = 'GNU GPL',
    name = 'ardj',
    package_dir = {'': 'src'},
    packages = ['ardj', 'ardj.xmpp'],
    install_requires = ['PyYAML', 'mutagen', 'pydns', 'oauth2', 'web.py'],
    scripts = ['bin/ardj', 'bin/ardj-next-track', 'bin/ezstream-meta'],
    url = 'http://umonkey.net/ardj/',
    version = '1.2.10'
)
