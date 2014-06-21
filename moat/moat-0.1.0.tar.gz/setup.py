#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

setup(
    name='moat',
    version='0.1.0',
    author='Joël Cox',
    author_email='joel@joelcox.nl',
    packages=['moat'],
    scripts=[],
    url='https://github.com/joelcox/moat',
    license='MIT',
    description='A simple authorization API for Python.',
    long_description=open('README.rst').read(),
    install_requires=[
        'enum34 == 1.0',
    ],
)