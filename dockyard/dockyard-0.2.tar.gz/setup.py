#!/usr/bin/env python

from setuptools import setup, find_packages


with open('README.txt') as file:
    long_description = file.read()

setup(name='dockyard',
        version='0.2',
        description='Light-weight CLI for development using Vagrant + Docker',
        long_description=long_description,
        author='Joshua Bellamy-Henn',
        author_email='josh@psidox.com',
        url='https://github.com/smysnk/dockyard',
        install_requires=['python-vagrant>=0.5.0', 'docker-py>=0.3.2'],
        keywords="docker vagrant dockyard",
        packages=find_packages(),
        entry_points={
            'console_scripts':
                ['dockyard = dockyard.entry:main'],
        }
    )