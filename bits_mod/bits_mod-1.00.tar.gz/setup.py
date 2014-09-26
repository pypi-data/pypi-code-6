
import os

from setuptools import setup, find_packages

setup(
    name = "bits_mod",
    version = "1.00",
    py_modules = ['bits_mod'],

    # metadata for upload to PyPI
    author = "Daniel Richard Stromberg",
    author_email = "strombrg@gmail.com",
    description='Pure Python efficient array of bits',
    long_description='''
A Pure Python bit array is provided.

It passes pylint, passes pep8, is thoroughly unit tested, and runs on CPython 2.[4567], CPython 3.[01234],
Pypy 2.4.0, Pypy3 2.3.1 and Jython 2.7b3.

It adapts to different "long" lengths, so it is not wasteful with 32 bit or 64 bit longs.
''',
    license = "Apache v2",
    keywords = "Bit Array List",
    url='http://stromberg.dnsalias.org/~strombrg/bits_mod/',
    platforms='Cross platform',
    classifiers=[
         "Development Status :: 5 - Production/Stable",
         "Intended Audience :: Developers",
         "Programming Language :: Python :: 2",
         "Programming Language :: Python :: 3",
         ],
)

