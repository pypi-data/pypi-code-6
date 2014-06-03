#!/usr/bin/env python
#    -*- coding: utf-8 -*-
import os

import jsonl

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

#    allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="jsonl",
    version=jsonl.__version__,
    url='https://bitbucket.org/sys-git/jsonl',
        packages=find_packages(exclude='test'),
    author=jsonl.__author__,
    author_email=jsonl.__email__,
    description='JSON decoding to mutable or immutable objects allowing attribute access',
    license="GNU General Public License",
    platforms=['any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=True,
    install_requires=['simplejson']
)

