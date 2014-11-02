#!/usr/bin/python
"""
Install PlexAPI
"""
from distutils.core import setup
from pip.req import parse_requirements
from setuptools import find_packages

# Fetch the current version
with open('plexapi/__init__.py') as handle:
    for line in handle.readlines():
        if line.startswith('VERSION'):
            VERSION = line.split('=')[1].strip(" '\n")

# Parse the requirements file
requirements = [str(line.req) for line in parse_requirements('requirements.pip')]

setup(
    name='PlexAPI',
    version=VERSION,
    description='Python bindings for the Plex API.',
    author='Michael Shepanski',
    author_email='mjs7231@gmail.com',
    url='http://bitbucket.org/mjs7231/plexapi',
    packages=find_packages(),
    install_requires=requirements,
    long_description=open('README.md').read()
)
