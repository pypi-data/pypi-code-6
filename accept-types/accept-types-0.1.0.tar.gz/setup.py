#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='accept-types',
    version="0.1.0",
    description='Determine the best content to send in an HTTP response',
    long_description=readme,
    author='Tim Heap',
    author_email='tim@timheap.me',
    url='https://bitbucket.org/tim_heap/python-accept-types',
    packages=find_packages(),
    package_data={},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
