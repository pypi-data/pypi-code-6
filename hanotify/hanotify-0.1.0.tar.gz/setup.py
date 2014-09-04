import os
import logging
import getpass

from setuptools import setup

logging.basicConfig(level=logging.INFO)

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "hanotify",
    version = "0.1.0",
    author = "Benjamin Wallis",
    author_email = "ben.nat.wallis@gmail.com",
    description = ("An email notification tool for hockey app crash reports"),
    license = "BSD",
    keywords = "hockeyapp crash hanotify",
    packages=['hanotifylib'],
    scripts=['hanotify'],
    long_description=read('README.md'),
    install_requires=[
        'mandrill==1.0.56',
        'logging==0.4.9.6',
        'hockeylib==0.1.0'
    ]
)
