import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "cvxfit",
    version = "0.1.5",
    author = "Mainak Chowdhury, Alon Kipnis, Milind Rao",
    author_email = "mainakch@gmail.com",
    description = ("A package for fitting convex functions to data. "),
    license = "BSD",
    keywords = "convex fit",
    url = "http://packages.python.org/cvxfit",
    packages=['cvxfit'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
    ],
    install_requires=['scipy>=0.13.0'],
)
