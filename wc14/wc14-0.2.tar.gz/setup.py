#!/usr/bin/env python

__author__ = "Alok Kumar"

from setuptools import setup, find_packages

setup(
    name="wc14",
    version="0.2",
    author="Alok Kumar",
    author_email="rajalokan@gmail.com",
    url="https://github.com/rajalokan/wc14",
    download_url="https://github.com/rajalokan/wc14/archive/0.1.tar.gz",
    description=("Command line tool to keep you updated about Football world cup 2014."),
    packages=find_packages(),
    include_package_data=True,
    install_requires=['click', 'requests', 'colorama', 'humanize'],
    entry_points='''
        [console_scripts]
        wc14=wc14.cli:cli
    ''',
)
