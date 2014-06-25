#!/usr/bin/python
# -*- coding: utf-8 -*-


from distutils.core import setup


setup(
    name="pysed",
    version="0.1.5",
    description="Utility that parses and transforms text",
    keywords=["python", "sed", "unix", "linux", "text",
                "stream", "editor"],
    author="dslackw",
    author_email="d.zlatanidis@gmail.com",
    url="https://github.com/dslackw/pysed",
    scripts=["bin/pysed"],
    package_data={"": ["LICENSE", "README.rst", "CHANGELOG"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: MS-DOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows Vista",
        "Operating System :: Microsoft :: Windows :: Windows XP",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: Other",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Text Editors",
        "Topic :: Text Editors :: Text Processing",
        "Topic :: Text Editors :: Word Processors",
        "Topic :: Text Processing",
        "Classifier: Topic :: Utilities"],
    long_description=open("README.rst").read()
)
