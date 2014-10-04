#!/usr/bin/env python

import sys
import os
from setuptools import setup

DESC = """A Python Package to infer ages using US Census Data"""

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

LONG_DESC = read("README.md")

setup(
    name="demographica",
    version='0.1.3',
    description=DESC,
    long_description=LONG_DESC,
    author="Cameron Davidson-Pilon",
    author_email="cam.davidson.pilon@gmail.com",
    license="MIT",
    packages=["demographica"],
    url="https://github.com/CamDavidsonPilon/demographica",
    install_requires=["numpy", "pandas>=0.14", "matplotlib"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
    ],
)
