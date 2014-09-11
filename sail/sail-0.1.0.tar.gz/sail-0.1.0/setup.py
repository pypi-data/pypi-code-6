#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "sail",
    version = "0.1.0",
    author = "Vincent Giersch, Jean-Tiare Le Bigot",
    author_email = "sail@sailabove.com",
    description = ("Sailabove CLI - Docker hosting"),
    license = "BSD",
    keywords = "cloud sailabove cli docker hosting",
    url = "http://labs.runabove.com/",
    packages = find_packages(),
    scripts = [
        'sail'
    ],
    install_requires = [
        'docutils>=0.3',
        'tabulate==0.7.2',
        'python-dateutil==2.2',
        'requests==2.3.0',
        'argparse==1.2.1',
    ],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: System",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)


