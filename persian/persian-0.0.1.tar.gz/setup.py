import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "persian",
    version = "0.0.1",
    author = "Mohammad Reza Kamalifard",
    author_email = "mr.kamalifard@gmail.com",
    description = ("A simple Python library for Persian language localization"),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "http://packages.python.org/persian",
    packages=['persian'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python"
    ],
)
