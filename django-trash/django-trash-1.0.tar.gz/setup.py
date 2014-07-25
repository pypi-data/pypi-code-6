import os
from setuptools import setup, find_packages

setup(
	name = 'django-trash',
	version = '1.0',
	url = '',
	license = 'BSD',
	description = 'DB trash, app for django',
	author = 'Kiel Labian',
	packages = find_packages('src'),
	package_dir = {'': 'src'},
	install_requires = ['setuptools'],
)