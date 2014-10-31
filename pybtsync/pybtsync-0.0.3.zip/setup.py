#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name = "pybtsync",
    version = "0.0.3",
    description = "A Python module for the BitTorrent Sync API.",
    long_description = "A Python module for the BitTorrent Sync API.",
    author = "Tiago Macarios",
    author_email = "tiagomacarios <at> the google email",
    url = "https://github.com/tiagomacarios/pybtsync",
    download_url = "https://github.com/tiagomacarios/pybtsync",
    py_modules = ['pybtsync'],
    scripts = ['pbts'],
    install_requires = ['requests', 'docopt'],
    license = "MIT",
    keywords = "bittorrent sync api",
    classifiers = [ "Development Status :: 3 - Alpha",
                    "Environment :: Console",
                    "Intended Audience :: Developers",
                    "License :: OSI Approved :: MIT License",
                    "Natural Language :: English",
                    "Operating System :: OS Independent",
                    "Programming Language :: Python",
                    "Topic :: Internet",
                    "Topic :: Software Development",
                    "Topic :: Utilities",
                    ] # https://pypi.python.org/pypi?%3Aaction=list_classifiers                    
)
