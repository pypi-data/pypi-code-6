
import os

from setuptools import setup, find_packages

setup(
    name = "dupdict_mod",
    version = "1.0",
    py_modules = ['dupdict_mod'],

    # metadata for upload to PyPI
    author = "Daniel Richard Stromberg",
    author_email = "strombrg@gmail.com",
    description='Pure Python dictionary wrapper that allows duplicates',
    long_description='''
A Pure Python dictionary wrapper that allows duplicate keys is provided.

It passes pylint, passes pep8, is thoroughly unit tested, and runs on CPython 2.[67], CPython 3.[01234],
Pypy 2.4.0, Pypy3 2.3.1 and Jython 2.7b3.
''',
    license = "Apache v2",
    keywords = "dictionary duplicate keys",
    url='http://stromberg.dnsalias.org/~strombrg/dupdict_mod/',
    platforms='Cross platform',
    classifiers=[
         "Development Status :: 5 - Production/Stable",
         "Intended Audience :: Developers",
         "Programming Language :: Python :: 2",
         "Programming Language :: Python :: 3",
         ],
)

