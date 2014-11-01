from setuptools import setup, find_packages

README = """
Python client for logFaces.

This is basically just the client written by Stojan Jovic that can be found on the 
logFaces download page, only with a setup.py file for easier installation.

http://www.moonlit-software.com/logfaces/web/download/

Currently requires setuptools.  The setup script hasn't been tested with python 
versions other than 2.7.

To install:

    pip install pylogfaces

And you're done.


"""

setup(
    name="pylogfaces",
    version="1.0.1",
    description="Logging utilities for logFaces and python.",
    long_description=README,
    author="Stojan Jovic",
    author_email="send_me_spam@yahoo.com",
    url="https://github.com/nickswebsite/pylogfaces",
    packages=find_packages(),
)

