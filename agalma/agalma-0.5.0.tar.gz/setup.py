#!/usr/bin/env python

import hashlib
import os
import sys
import urllib2
import zipfile
from glob import glob
from distutils.command.build_scripts import build_scripts
from distutils.errors import DistutilsFileError
from setuptools import setup
from setuptools.command.install import install

# get __version__
execfile("agalma/__init__.py")

scripts = glob("scripts/agalma*")
scripts.append("scripts/agalma-test-tutorial")

class _build_scripts(build_scripts):
    def run(self):
        print "generating agalma-test-tutorial from TUTORIAL.md"
        with open("scripts/agalma-test-tutorial", 'w') as f:
            f.write(open("scripts/stub.agalma-test-tutorial").read())
            for line in open("TUTORIAL.md"):
                if line.startswith("    "):
                    f.write(line[4:])
        build_scripts.run(self)

blastdb = {
    "url": "https://bitbucket.org/caseywdunn/agalma/downloads/agalma-blastdb-0.5.0.zip",
    "md5": "1ffd6b32bb233e315c6695636491c318",
    "size": 136,
    "subdir": "blastdb"}

testdata = {
    "url": "https://bitbucket.org/caseywdunn/agalma/downloads/agalma-testdata-0.4.0.zip",
    "md5": "aeec822e72ad5c6bf75297d38110f612",
    "size": 11,
    "subdir": "testdata"}

md5_error = """
The downloaded file:
%s
has an incorrect MD5 sum and is corrupt.
Please remove the file and try again."""

def _md5sum(path):
    chunks = hashlib.md5()
    # Build hash from 64KB chunks of the binary file.
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), ''):
            chunks.update(chunk)
    return chunks.hexdigest()

def _install_data(data, dst):
    """
    Download a zip file, check its MD5 hash, and unzip it into `dst`.
    """
    if os.path.exists(os.path.join(dst, data["subdir"])):
        print "+ Already installed."
        return
    dl = os.path.abspath(os.path.basename(data["url"]))
    # download
    if not os.path.exists(dl):
        print "+ Downloading zip file (%dMB):" % data["size"]
        print "| ",
        request = urllib2.urlopen(data["url"])
        with open(dl, 'w') as f:
            while True:
                chunk = request.read(1048576)
                if chunk:
                    f.write(chunk)
                    sys.stdout.write('=')
                    sys.stdout.flush()
                else:
                    print " done"
                    break
    # check md5
    print "+ Checking MD5 sum...",
    if _md5sum(dl) != data["md5"]:
        raise DistutilsFileError(md5_error % dl)
    print "done"
    # unzip
    print "+ Unzipping...",
    zipfile.ZipFile(dl).extractall(path=dst)
    print "done"

class _install(install):
    def run(self):
        install.run(self)
        dst = os.path.join(self.install_lib, "agalma")
        self.execute(
            _install_data, (blastdb, dst),
            msg="Installing custom Agalma blast databases...")
        self.execute(
            _install_data, (testdata, dst),
            msg="Installing Agalma test data...")

setup(
    name="agalma",
    version=__version__,
    author="Mark Howison",
    author_email="mhowison@brown.edu",
    url="https://bitbucket.org/caseywdunn/agalma",
    description="""
        An automated phylogenomics pipeline.""",
    long_description="""
        Agalma is an automated tool that constructs matrices for
        phylogenomic analyses, allowing complex phylogenomic analyses to be
        implemented and described unambiguously as a series of high-level
        commands.  The user provides raw Illumina transcriptome data, and
        Agalma produces annotated assemblies, aligned gene sequence matrices,
        a preliminary phylogeny, and detailed diagnostics that allow the
        investigator to make extensive assessments of intermediate analysis
        steps and the final results.  Sequences from other sources, such as
        externally assembled genomes and transcriptomes, can also be
        incorporated in the analyses. Agalma is built on the BioLite
        bioinformatics framework, which tracks provenance, profiles processor
        and memory use, records diagnostics, manages metadata, installs
        dependencies, logs version numbers and calls to external programs, and
        enables rich HTML reports for all stages of the analysis. Agalma
        includes a small test data set and a built-in test analysis of these
        data.""",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics"],
    provides=["agalma"],
    requires=["biolite (==0.5.0)"],
    install_requires=["biolite==0.5.0"],
    packages=["agalma"],
    package_data={"agalma": ["config/*", "data/*"]},
    scripts=scripts,
    cmdclass={"build_scripts": _build_scripts, "install": _install}
)
