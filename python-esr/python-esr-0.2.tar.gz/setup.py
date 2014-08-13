#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='python-esr',
    version='0.2',
    author='Leuchter Open Source Solutions AG',
    author_email='tryton@leuchterag.ch',
    url='https://bitbucket.org/loss/python-esr',
    description='Swiss ESR account statement record parser',
    long_description=read('README'),
    packages=find_packages(),
    package_data={
        'tests': ['data/*.v11'],
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Accounting',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    license='GPL-3',
    test_suite='tests',
    zip_safe=False,
    )
