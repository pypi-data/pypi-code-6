#!/usr/bin/env python2
from setuptools import setup, find_packages
from distutils.util import convert_path
from distutils.command.install import INSTALL_SCHEMES
import os, sys, glob

setup(
    name                 = 'pwn',
    packages             = [],
    install_requires     = ['pwntools'],
    version              = '1.0',
    description          = "This is the CTF framework used by Gallopsled in every CTF.",
    author               = "Gallopsled et al.",
    author_email         = "#gallopsled @ freenode.net",
    url                  = 'https://github.com/Gallopsled/pwntools/',
    download_url         = "https://github.com/Gallopsled/pwntools/tarball/master",

    license              = "Mostly MIT, some GPL/BSD, see LICENSE-pwntools.txt",
    classifiers          = [
        'Topic :: Security',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers'
    ]
)
