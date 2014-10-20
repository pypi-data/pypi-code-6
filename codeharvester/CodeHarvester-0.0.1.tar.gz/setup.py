# -*- coding: utf-8 -*-

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "CodeHarvester",
    version = "0.0.1",
    author = "Denis Gonsiorovsky",
    author_email = "dns.gnsr@gmail.com",
    description = ("A tool to merge an input file and all of its requirements into a single output file. Similar to Sprockets."),
    license = "BSD",
    keywords = "python js sprockets requirements dependencies merge join",
    url = "http://packages.python.org/codeharvester",
    packages=['codeharvester'],
    package_dir={
        'codeharvester': 'src/codeharvester'
    },
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Utilities",
    ],
    scripts=['src/harvester.py']
)