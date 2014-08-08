# -*- coding: utf-8 -*-
import os.path

from setuptools import setup


def readme():
    path = os.path.join(os.path.dirname(__file__), 'README')
    with open(path, 'rU') as fin:
        return fin.read()


setup(
    name='omt',
    version='0.1.0',
    author='Tyler Kennedy',
    author_email='tk@tkte.ch',
    long_description=readme(),
    description='Tools for turning terminal sessions into JSON/HTML.',
    packages=[
        'omt'
    ],
    include_package_data=True,
    package_data={
        'omt': ['templates/*']
    },
    url='http://github.com/tktech/omt',
    entry_points={
        'console_scripts': [
            'omt-py = omt.cli:from_cli',
        ]
    },
    install_requires=[
        'docopt',
        'pyte',
        'jinja2'
    ]
)
