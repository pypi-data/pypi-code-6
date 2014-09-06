from setuptools import setup, find_packages # Always prefer setuptools over distutils
from codecs import open # To use a consistent encoding
from os import path
here = path.abspath(path.dirname(__file__))
setup(
	name='gmapsbounds',
	# Versions should comply with PEP440. For a discussion on single-sourcing
	# the version across setup.py and the project code, see
	# http://packaging.python.org/en/latest/tutorial.html#version
	version='0.0.9.1',
	description='Extract Lat/Lng boundary points of geographical regions from Google Maps',
	# The project's main homepage.
	url='https://github.com/evfredericksen/gmapsbounds',
	# Author details
	author='Evan Fredericksen',
	author_email='evfredericksen@gmail.com',
	# Choose your license
	license='MIT',
	# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
	classifiers=[
	'Development Status :: 3 - Alpha',
	# Indicate who your project is intended for
	'Intended Audience :: Developers',
	'Topic :: Software Development :: Build Tools',
	# Pick your license as you wish (should match "license" above)
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 2',
	'Programming Language :: Python :: 2.6',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.2',
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	],
	# What does your project relate to?
	keywords='google maps lat lng boundaries',
	packages=['gmapsbounds'],
	package_dir = {
		'gmapsbounds': 'gmapsbounds',
	},
	install_requires=['selenium'],
	scripts = ['scripts/gmapsbounds.py'],
	# entry_points={
	# 	'console_scripts': [
	# 	'sample=sample:main',
	# 	],
	# },
	include_package_data = True,
	 long_description = '''\
	Use Google Maps web app and API to find lat/lng boundaries of
	geographical regions, including cities, ZIP codes, counties,
	states and countries.
	'''
)