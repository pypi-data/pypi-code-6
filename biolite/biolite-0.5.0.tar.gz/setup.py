#!/usr/bin/env python

from glob import glob
from setuptools import setup

# get __version__
execfile("biolite/__init__.py")

setup(
    name="biolite",
    version=__version__,
    author="Mark Howison",
    author_email="mhowison@brown.edu",
    url="https://bitbucket.org/caseywdunn/biolite",
    description="""
        A lightweight bioinformatics framework with automated tracking of
        diagnostics and provenance.""",
    long_description="""
        BioLite is a bioinformatics framework that automates the
        collection and reporting of diagnostics, tracks provenance, and
        provides lightweight tools for building custom analysis pipelines.""",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Bio-Informatics"],
    provides=["biolite"],
    requires=[
        "biopython (>=1.60)",
        "dendropy (>=3.12.0)",
        "docutils (>=0.9.1)",
        "lxml (>=3.2.1)",
        "matplotlib (>=1.1.0)",
        "networkx (>=1.6)",
        "numpy (>=1.6.1)",
        "wget (>=2.0)"],
    install_requires=[
        "biopython>=1.60",
        "dendropy>=3.12.0",
        "docutils>=0.9.1",
        "lxml>=3.2.1",
        "matplotlib>=1.1.0",
        "networkx>=1.6",
        "numpy>=1.6.1",
        "wget>=2.0"],
    packages=["biolite", "biolite.workflows"],
    package_data={"biolite": ["config/*", "data/*"]},
    scripts=glob("scripts/bl-*")
)
