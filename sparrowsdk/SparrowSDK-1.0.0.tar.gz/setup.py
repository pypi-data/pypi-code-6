#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='SparrowSDK',
    version='1.0.0',
    author='Sparrow SMS',
    author_email='developers@sparrowsms.com',
    packages=find_packages(),
    scripts=['bin/sparrowsms.py',],
    url='http://api.sparrowsms.com/',
    license='',
    description='Python SDK for Sparrow SMS API.',
    long_description=open('README.rst').read(),
    install_requires=[
        "requests",
    ],
)
