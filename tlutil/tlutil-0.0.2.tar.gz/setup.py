#!/usr/bin/python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


PACKAGE = "tlutil"
NAME = "tlutil"
DESCRIPTION = "tuoluo tool package"
AUTHOR = "zwczou"
AUTHOR_EMAIL = "zwczou@gmail.com"
URL = "http://github.com/zakzou/tlutil"
VERSION = __import__(PACKAGE).__version__


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description="see http://github.com/zakzou/tlutil",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "simplejson",
        "flask",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Flask",
    ],
    zip_safe=False,
)
