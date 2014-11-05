#!/bin/env python
# -*- coding: utf8 -*-

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

version = "0.1.0"

setup(
    name="python-webnews",
    version=version,
    description="CSH webnews library",
    classifiers=[],
    keywords="csh webnews",
    author="ahanes",
    author_email="ahanes@csh.rit.edu",
    url="https://github.com/AndrewHanes/Python-Webnews",
    license="None",
    packages=find_packages(),
    scripts=[
        "distribute_setup.py",
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "",
    ],
    #TODO: Deal with entry_points
    #entry_points="""
    #[console_scripts]
    #pythong = pythong.util:parse_args
    #"""
)
