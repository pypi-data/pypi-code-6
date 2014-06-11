#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'pysed',
    version = "0.0.3",
    description = "Utility that parses and transforms text",
    keywords = ["python", "sed", "unix", "linux", "text", 
		"stream", "editor"],
    author = "dslackw",
    author_email = "d.zlatanidis@gmail.com",
    url = "https://github.com/dslackw/pysed",
    scripts = ['bin/pysed'],
    package_data = {"": ["LICENSE", "README.rst", "CHANGELOG"]},
    classifiers = [
	"Classifier: Development Status :: 3 - Alpha",
	"Classifier: Environment :: Console",
	"Classifier: License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
	"Classifier: Operating System :: POSIX",
	"Classifier: Operating System :: POSIX :: Linux",
	"Classifier: Operating System :: Unix",
	"Classifier: Programming Language :: Python",
	"Classifier: Programming Language :: Python :: 2.7",
	"Classifier: Programming Language :: Unix Shell",
	"Classifier: Topic :: Text Editors",
	"Classifier: Topic :: Text Editors :: Text Processing",
	"Classifier: Topic :: Text Processing",
	"Classifier: Topic :: Text Processing :: General",
	"Classifier: Topic :: Utilities"],
    long_description=open("README.rst").read()
)
