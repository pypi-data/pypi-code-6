#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'pysed',
    version = "0.0.1",
    description = "Utility that parses and transforms text",
    keywords = ["python", "sed", "unix", "linux", "text", 
"stream", "editor"],
    author = "dslackw",
    author_email = "d.zlatanidis@gmail.com",
    url = "https://github.com/dslackw/pysed",
    scripts = ['bin/pysed'],
    package_data = {"": ["LICENSE", "README.rst", "CHANGELOG"]},
    classifiers = [
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 3 - Alpha",
        "Topic :: Intersetup.pynet :: Utilities"],
    long_description=open("README.rst").read()
)
