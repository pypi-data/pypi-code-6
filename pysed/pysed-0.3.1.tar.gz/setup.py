#!/usr/bin/python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pysed import __version__
from pysed import __email__

setup(
    name="pysed",
    packages=['pysed'],
    scripts=["bin/pysed"],
    version=__version__,
    description="Utility that parses and transforms text",
    keywords=["python", "sed", "unix", "linux", "text",
                "stream", "editor"],
    author="dslackw",
    author_email=__email__,
    url="https://github.com/dslackw/pysed",
    package_data={"": ["LICENSE", "README.rst", "CHANGELOG"]},
    classifiers=[
        "Development Status :: 3 - Alpha"
        "Environment :: Console"
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        "Operating System :: Microsoft :: MS-DOS"
        "Operating System :: Microsoft :: Windows"
        "Operating System :: Microsoft :: Windows :: Windows 7"
        "Operating System :: Microsoft :: Windows :: Windows Vista"
        "Operating System :: Microsoft :: Windows :: Windows XP"
        "Operating System :: POSIX"
        "Operating System :: POSIX :: BSD :: BSD/OS"
        "Operating System :: POSIX :: BSD :: FreeBSD"
        "Operating System :: POSIX :: Linux"
        "Operating System :: POSIX :: Other"
        "Operating System :: Unix"
        "Programming Language :: Python"
        "Programming Language :: Python :: 2"
        "Programming Language :: Python :: 2.6"
        "Programming Language :: Python :: 2.7"
        "Programming Language :: Python :: 3"
        "Programming Language :: Python :: 3.0"
        "Programming Language :: Python :: 3.1"
        "Programming Language :: Python :: 3.2"
        "Programming Language :: Python :: 3.3"
        "Programming Language :: Python :: 3.4"
        "Topic :: Text Editors"
        "Topic :: Text Editors :: Documentation"
        "Topic :: Text Editors :: Text Processing"
        "Topic :: Text Editors :: Word Processors"
        "Topic :: Text Processing :: Filters"
        "Topic :: Text Processing :: General"
        "Topic :: Utilities"
        "Classifier: Topic :: Utilities"],
    long_description=open("README.rst").read()
)
