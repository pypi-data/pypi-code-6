from setuptools import setup, find_packages
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))

setup(
	name='gmapsbounds',
	version='0.1.5',
	description='Extract Lat/Lng boundary points of geographical regions from Google Maps',
	url='https://github.com/evfredericksen/gmapsbounds',
	author='Evan Fredericksen',
	author_email='evfredericksen@gmail.com',
	license='MIT',
	classifiers=[
	'Development Status :: 3 - Alpha',
	'Intended Audience :: Developers',
	'Topic :: Software Development :: Build Tools',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 2',
	'Programming Language :: Python :: 2.6',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.2',
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	],
	keywords='google maps lat lng boundaries',
	packages=['gmapsbounds'],
	package_dir = {
		'gmapsbounds': 'gmapsbounds',
	},
	install_requires=['selenium'],
	scripts = ['scripts/gmapsbounds'],
	include_package_data = True,
	long_description = '''\
	Use Google Maps web app to find lat/lng boundaries of
	geographical regions, including cities, ZIP codes, counties,
	states and countries.
	'''
)