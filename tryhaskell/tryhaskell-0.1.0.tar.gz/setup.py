#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="tryhaskell",
    version="0.1.0",
    author="Cary Robbins",
    author_email="carymrobbins@gmail.com",
    url="https://github.com/carymrobbins/py-tryhaskell",
    packages=find_packages(),
    description="Python client for tryhaskell.org",
    license='BSD3',
    install_requires=[
        'requests',
    ],
    classifiers=[
    ]
)
