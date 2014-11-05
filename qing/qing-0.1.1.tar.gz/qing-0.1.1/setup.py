#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import setuptools
except ImportError:
    import distutils.core as setuptools


__author__ = 'Qing Dev'
__copyright__ = 'Copyright 2014'
__credits__ = []

__version__ = '0.1.1'
__maintainer__ = 'Qing Dev'
__email__ = 'qingup.io@gmail.com'

__title__ = 'qing'
__build__ = 0x000000

__url__ = 'https://github.com/qingup/qing'
__description__ = 'Lightweight ops tool'

setuptools.setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    maintainer=__maintainer__,
    maintainer_email=__email__,
    url=__url__,
    description=__description__,
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Operating System :: OS Independent',
                 'Topic :: Utilities'],
    platforms=['Independent'],
    packages=['qing'],
    install_requires=[
    ],
    zip_safe=True,
)

