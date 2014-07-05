#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

#    Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

import depends

setup(
    name = "depends",
    version = depends.__version__,
    url = 'https://bitbucket.com/sys-git/depends',
    packages = find_packages(),
    package_dir = {'depends': 'depends'},
    include_package_data = False,
    author = depends.__author__,
    author_email = depends.__email__,
    description = "A pure-python dependency linker and checker",
    license = "GNU General Public License",
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications',
    ]
)
