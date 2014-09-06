# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4",
    "Topic :: Software Development",
    "Topic :: Software Development :: Documentation",
    "Topic :: Text Processing :: Markup",
]

setup(
    name='sphinxjp.usaturn',
    version='0.2.0',
    description='a sphinx extension to add new admonition named `usaturn`',
    long_description=open("README.rst").read(),
    classifiers=classifiers,
    keywords=['document'],
    author='Takeshi Komiya',
    author_email='i.tkomiya at gmail.com',
    url='http://bitbucket.com/tk0miya/sphinxjp.usaturn',
    download_url='http://pypi.python.org/pypi/sphinxjp.usaturn',
    license='Apache License 2.0',
    packages=find_packages(),
)
