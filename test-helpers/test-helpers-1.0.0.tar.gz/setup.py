#!/usr/bin/env python
import sys

from setuptools import setup, find_packages

VERSION = '1.0.0'

def read_requirements_file(filename):
    """Read pip-formatted requirements from a file."""
    with open(filename, 'r') as f:
        return [
            line.strip() for line in f.readlines()
            if not line.startswith('#')
        ]


setup(
    name='test-helpers',
    description='A collection of test helpers to facilitate AAA testing.',
    packages=find_packages(exclude=['tests', 'tests.*']),
    test_suite='nose.collector',
    include_package_data=True,
    zip_safe=False,
    long_description='''
        A collection of test helpers to facilitate class-based AAA testing.
    ''',
    install_requires=read_requirements_file('requirements.txt'),
    tests_require=read_requirements_file('dev-requirements.txt'),
    version=VERSION,
    author='AWeber Communications',
    author_email='api@aweber.com',
    entry_points={'console_scripts': []},
    extras_require={'tornado': ['tornado>=3.1']}
)
