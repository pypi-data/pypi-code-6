# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:noexpandtab
# c-basic-indent: 4; tab-width: 4; indent-tabs-mode: true;
import sys

import setuptools

setup_params = dict(
	name="bdt_sitemap",
	version='0.9.0',
	packages=setuptools.find_packages(),
	include_package_data=True,
	entry_points=dict(
		console_scripts = [
			'bdt_sitemap=bdt.sitemap:run_shell',
		],
	),
	install_requires=[
		"beautifulsoup4",
	],
	description="Sitemap Generator - Walks a local directory and its contents, generating sitemaps as it goes",
	license = 'AGPL3+',
	author="Daniel Tadeuszow",
	author_email="dtadeuszow@gmail.com",
	url = 'http://github.com/xenmen/bdt_sitemap',
	classifiers=[
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Operating System :: POSIX',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: MacOS :: MacOS X',
		'Programming Language :: Python :: 2.7',
		'Intended Audience :: Developers',
		'Intended Audience :: System Administrators',
		'Topic :: Communications :: Chat :: Internet Relay Chat',
		'Topic :: Internet :: WWW/HTTP',
		'Topic :: Software Development',
		'Topic :: Text Processing :: Indexing',
		'Topic :: Text Processing :: Markup :: HTML',
		'Topic :: Text Processing :: Markup :: XML',
		'Topic :: Utilities',
	],
	long_description = open('README.txt').read(),
)	#keywords: sitemap, sitemap generator, sitemap.xml

if __name__ == '__main__':
	setuptools.setup(**setup_params)
