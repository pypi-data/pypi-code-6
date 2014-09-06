# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(
    name="mtgtransform",
    version="0.0.4",
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,

    author="Børge Lanes",
    author_email="borge.lanes@gmail.com",
    description=("Magic the Gathering deck transformator."),
    long_description=read("README.md"),
    license="MIT",
    keywords="mtg",
    url="https://github.com/leinz/mtgtransform",

    entry_points={
        'console_scripts': [
            'mtgtransform=mtgtransform.main:main'
        ]
    }
)
