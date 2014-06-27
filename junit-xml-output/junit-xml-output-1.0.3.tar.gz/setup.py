#!/usr/bin/env python
from setuptools import setup, find_packages
import os


def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='junit-xml-output',
	author = 'David Black',
	author_email = 'dblack@atlassian.com',
	url = 'https://bitbucket.org/db_atlass/python-junit-xml-output-module',
	packages = find_packages(),
	description = read('README.txt'),
	long_description = read('README.txt'),
	license = "MIT",
	version = __import__('junit_xml_output').__version__,
	test_suite = 'junit_xml_output.test',
	platforms=['any'],
	classifiers = [
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
	],
)

