# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name="strict",
    version="0.1alpha",
    packages=["strict"],
    license="MIT",
    description="",
    long_description=open("README.txt").read(),
    author="Jevgeni Tarassov",
    author_email="jevgeni@tarasov.ch",
    url="https://bitbucket.org/slenderboy/strict",
    install_requires=[
        "six >= 1.7.3"
    ]
)