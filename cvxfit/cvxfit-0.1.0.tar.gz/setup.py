import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "cvxfit",
    version = "0.1.0",
    author = "Mainak Chowdhury, Alon Kipnis, Milind Rao",
    author_email = "mainakch@gmail.com",
    description = ("A package for fitting convex functions to data. "),
    license = "BSD",
    keywords = "convex fit",
    url = "http://packages.python.org/cvxfit",
    packages=['cvxfit'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=['docutils>=0.3','scipy>=0.13.0'],
)
