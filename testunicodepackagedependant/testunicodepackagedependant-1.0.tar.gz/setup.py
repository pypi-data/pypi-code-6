#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="testunicodepackagedependant",
    version="1.0",
    description="Test package dependant on a package with Unicode filenames",
    long_description=open('README.rst', 'rb').read(),
    author="Lukasz Langa",
    author_email="lukasz@langa.pl",
    url="http://pypi.python.org/pypi/testunicodepackagedependant/",
    license="MIT",
    py_modules=['testunicodepackagedependant'],
    package_dir={'': 'src'},
    platforms="Any",
    install_requires=[
        "testunicodepackage==1.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
)

