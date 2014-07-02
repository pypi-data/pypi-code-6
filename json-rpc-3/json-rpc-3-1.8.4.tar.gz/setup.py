#!/usr/bin/env python3
import os
from setuptools import setup, find_packages
from jsonrpc import version


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ""

setup(
    name="json-rpc-3",
    version=version,
    packages=find_packages(),
    test_suite="nose.collector",
    tests_require=["nose", "mock"],
    author='see AUTHORS',
    maintainer='Orhideous',
    maintainer_email='orhideous@gmail.com',
    url="https://github.com/Orhideous/json-rpc",
    description="Pure Python 3 JSON-RPC 2.0 transport realisation",
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["json", "rpc", "json-rpc", "transport"],
    license="MIT",
)
