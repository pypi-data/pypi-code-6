
import os

from setuptools import setup, find_packages

setup(
    name = "fibonacci-heap-mod",
    version = "0.98",
    py_modules = ['fibonacci_heap_mod'],

    # metadata for upload to PyPI
    author = "Daniel Richard Stromberg",
    author_email = "strombrg@gmail.com",
    description='Pure Python Fibonacci Heap (Priority Queue)',
    long_description='''
A Pure Python Fibonacci Heap implementation of a Priority Queue is provided.

It passes pylint, passes pep8, is thoroughly unit tested, and runs on CPython 2.7, CPython 3.[01234],
Pypy 2.4.0, Pypy3 2.4.0 and Jython 2.7b3.
''',
    license = "Apache v2",
    keywords = "Fibonacci Heap, Priority Queue",
    url='http://stromberg.dnsalias.org/~strombrg/fibonacci-heap-mod/',
    platforms='Cross platform',
    classifiers=[
         "Development Status :: 5 - Production/Stable",
         "Intended Audience :: Developers",
         "Programming Language :: Python :: 2",
         "Programming Language :: Python :: 3",
         ],
)

