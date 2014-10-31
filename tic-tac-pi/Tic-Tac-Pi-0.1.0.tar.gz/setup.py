#!/bin/env python
# -*- coding: utf8 -*-

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

version = "0.1.0"

setup(
    name="Tic-Tac-Pi",
    version=version,
    description="Tic-Tac-Toe between two Raspberry Pis using PyGame",
    classifiers=[
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 2.7",
    ],
    keywords="PyGame Python Tic-Tac-Toe",
    author="mstubinis, Pharas",
    author_email="mst6119@rit.edu, bke2759@rit.edu",
    url="https://github.com/mstubinis/Tic-Tac-Pi",
    license="MIT",
    packages=find_packages(
    ),
    scripts=[
        "distribute_setup.py",
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "PyGame",
    ],
    #TODO: Deal with entry_points
    #entry_points="""
    #[console_scripts]
    #pythong = pythong.util:parse_args
    #"""
)