#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name="testunicodepackage",
    version="1.0",
    description="Test package with Unicode filenames",
    long_description=open('README.rst', 'rb').read(),
    author="Lukasz Langa",
    author_email="lukasz@langa.pl",
    url="http://pypi.python.org/pypi/testunicodepackage/",
    license="MIT",
    py_modules = ['testunicodepackage'],
    package_dir = {'': 'src'},
    platforms="Any",
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

