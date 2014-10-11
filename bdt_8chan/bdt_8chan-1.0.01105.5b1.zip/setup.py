# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:noexpandtab
# c-basic-indent: 4; tab-width: 4; indent-tabs-mode: true;
import sys

import setuptools

setup_params = dict(
	name="bdt_8chan",
	version='1.0.0',
	packages=setuptools.find_packages(),
	include_package_data=True,
	scripts = ['bdt/dl8chan.py', 'bdt/__init__.py'],
	entry_points=dict(
		console_scripts = [
			'b8=bdt:b8',
		],
	),
	install_requires=[
		"beautifulsoup4",
		"docopt >= 0.6.0",
	],
	description="8Chan Thread Archiver - Downloads a thread; images, webms and all.",
	license = 'AGPL3+',
	author="Daniel Tadeuszow",
	author_email="dtadeuszow@gmail.com",
	url = 'http://github.com/xenmen/bdt_8chan',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Operating System :: POSIX',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: MacOS :: MacOS X',
		'Programming Language :: Python :: 2.7',
		'Intended Audience :: Developers',
		'Intended Audience :: System Administrators',
		'Topic :: Internet :: WWW/HTTP',
		'Topic :: Text Processing :: Indexing',
		'Topic :: Text Processing :: Markup :: HTML',
		'Topic :: Utilities',
	],
	long_description = open('README.txt').read(),
)

if __name__ == '__main__':
	setuptools.setup(**setup_params)
