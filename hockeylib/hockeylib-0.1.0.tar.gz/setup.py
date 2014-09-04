import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "hockeylib",
    version = "0.1.0",
    author = "Benjamin Wallis",
    author_email = "ben.nat.wallis@gmail.com",
    description = ("A simple collection of hockey app api tools"),
    license = "BSD",
    keywords = "hockeyapp",
    packages=['hockeylib'],
    scripts=['hockey'],
    long_description=read('README.md'),
    install_requires=[
        'pycurl==7.19.3.1',
        'logging==0.4.9.6'
    ]
)