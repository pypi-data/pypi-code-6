#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pydouble',
    version='1.4.1',
    packages=find_packages(),
    url='https://github.com/jhautefeuille/pydouble',
    install_requires=["PySide"],
    include_package_data=True,
    license='BSD',
    author='Julien Hautefeuille',
    author_email='julien@hautefeuille.eu',
    description='Pydouble can find duplicated files.',
    classifiers=[
        "Programming Language :: Python",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
    ]
)
