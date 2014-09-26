# coding: utf-8
from setuptools import setup
import sys

if sys.version_info < (3,2):
	sys.stdout.write("At least Python 3.2 is required.\n")
	sys.exit(1)

__version__ = '1.0.1'

setup(
	name = 'chungpy',
	version = __version__,
	author = 'Corinna Ernst',
	author_email = 'corinna.ernst@uni-due.de',
	description = 'An implementation of Chung\'s linear-time algorithm for solution of the Maximum Density Segment Problem with extended applications',
	license = 'MIT',
	url = 'https://bitbucket.org/CorinnaErnst/chungpy',
	packages = {'chungpy'},
	install_requires=["numpy>=1.7"],
	classifiers = [
		"Development Status :: 4 - Beta",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: MIT License",
		"Natural Language :: English",
		"Programming Language :: Python :: 3",
		"Topic :: Scientific/Engineering :: Bio-Informatics"
	]
)

