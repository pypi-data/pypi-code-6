#!/usr/bin/env python
from setuptools import setup
from os import path

setup(
    name = 'bambu-gensite',
    version = '1.1',
    description = 'Fill a website with data generated from a YAML file',
    author = 'Steadman',
    author_email = 'mark@steadman.io',
    url = 'https://github.com/iamsteadman/bambu-gensite',
    long_description = open(path.join(path.dirname(__file__), 'README')).read(),
    install_requires = [
        'Django>=1.6',
        'requests>=2.0',
        'PyYAML>=3.10'
    ],
    packages = [
        'bambu_gensite',
        'bambu_gensite.management',
        'bambu_gensite.management.commands',
        'bambu_gensite.generators'
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django'
    ]
)
