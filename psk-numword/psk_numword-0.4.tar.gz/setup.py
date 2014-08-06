#!/usr/bin/env python
#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

import os
import re
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_version():
    init = read(os.path.join('numword', '__init__.py'))
    return re.search("__version__ = '([0-9.]*)'", init).group(1)


setup(name='psk_numword',
    version=get_version(),
    author='Presik Technologies',
    author_email='gerente@presik.com',
    url="https://bitbucket.org/presik/psk_numword",
    description="Python modules to convert numbers to words",
    download_url="https://bitbucket.org/presik/psk_numword/downloads",
    packages=find_packages(),
    test_suite='numword.tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: English',
        'Natural Language :: French',
        'Natural Language :: German',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
        'Topic :: Text Processing :: Linguistic',
        ],
    license='LGPL',
    use_2to3=True)
