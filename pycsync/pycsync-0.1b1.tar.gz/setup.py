#!/bin/env python
# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
Setup script for pycsync
'''

import os
from setuptools import setup

# Ensure we are in pycsync source dir
SETUP_DIRNAME = os.path.dirname(__file__)
if SETUP_DIRNAME != '':
    os.chdir(SETUP_DIRNAME)

PYCSYNC_VERSION = os.path.join(os.path.abspath(SETUP_DIRNAME),
                               'pycsync',
                               'version.py')
PYCSYNC_REQS = os.path.join(os.path.abspath(SETUP_DIRNAME),
                            'requirements.txt')

# pylint: disable=W0122
exec(compile(open(PYCSYNC_VERSION).read(), PYCSYNC_VERSION, 'exec'))
# pylint: enable=W0122

VER = __version__  # pylint: disable=E0602

REQUIREMENTS = []
with open(PYCSYNC_REQS) as rfh:
    for line in rfh.readlines():
        if not line or line.startswith('#'):
            continue
        REQUIREMENTS.append(line.strip())


SETUP_KWARGS = {
    'name': 'pycsync',
    'version': VER,
    'url': 'https://github.com/shadowfax-chc/pycsync',
    'license': 'ISC',
    'description': 'Sync local photos with Flickr',
    'author': 'Timothy F Messier',
    'author_email': 'tim.messier@gmail.com',
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        ('License :: OSI Approved ::'
         ' ISC License (ISCL)'),
        'Operating System :: POSIX :: Linux',
    ],
    'packages': ['pycsync'],
    'package_data': {},
    'data_files': [],
    'scripts': ['scripts/pycsync'],
    'install_requires': REQUIREMENTS,
    'zip_safe': False,
}

if __name__ == '__main__':
    setup(**SETUP_KWARGS)  # pylint: disable=W0142
