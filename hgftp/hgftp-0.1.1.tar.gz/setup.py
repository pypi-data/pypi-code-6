#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path

topdir = path.abspath(path.dirname(__file__))

with open(path.join(topdir, 'README.rst'), encoding='utf-8') as f:
	readme_text = f.read()
with open(path.join(topdir, 'CHANGES.rst'), encoding='utf-8') as f:
	changes_text = f.read()
long_description = readme_text + '\n' + changes_text

setup(
	name='hgftp',
	version='0.1.1',
	description='Upload snapshots of a revision to one or more FTP server',
	long_description=long_description,
	url='https://bitbucket.org/jaltek/hgftp',
	author='André Klitzing (misery)',
	author_email='andre@incubo.de',
	license='GPLv2+',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Plugins',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Topic :: Internet :: File Transfer Protocol (FTP)',
		'Topic :: Internet :: WWW/HTTP :: Site Management',
		'Topic :: Software Development',
	],
	keywords='mercurial ftp',
	packages=find_packages(),
	install_requires=['mercurial'],
)
