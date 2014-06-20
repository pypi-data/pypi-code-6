#!/usr/bin/env python
import setuptools
from setuptools import setup, find_packages
from distutils.core import setup

VERSION = "1.0"

setup(
    name = "wsgi-content-modifier",
    version = VERSION,
    author = 'Alan Justino da Silva',
    author_email = 'alan.justino@yahoo.com.br',
    url = 'http://github.com/alanjds/wsgi-content-modifier',
    #download_url = 'https://github.com/alanjds/django-moip/tarball/'+VERSION,
    install_requires = [],
    tests_require = [],
    test_suite = 'tests.suite',
    description = "A WSGI base for middlewares that modifies (transforms) the response",
    packages = find_packages(),
    include_package_data = True,
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)