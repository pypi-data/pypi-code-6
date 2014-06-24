#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

try:
    license = open('LICENSE').read()
except:
    license = None

try:
    readme = open('README.me').read()
except:
    readme = None

setup(
    name='just-columns',
    version='0.0.1',
    author='enalicho',
    author_email='enalicho@gmail.com',
    packages=['just-columns'],
    scripts=[],
    url='http://github.com/eeue56/just-columns',
    license=license,
    description='',
    long_description=readme,
    requires=['tornado'],
    install_requires=[
        'tornado >= 2.2.0'
    ]
)