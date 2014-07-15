#!/usr/bin/python3

# Copyright (C) 2012-2014 Cyrille Defranoux
#
# This file is part of Homewatcher.
#
# Homewatcher is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Homewatcher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Homewatcher. If not, see <http://www.gnu.org/licenses/>.
#
# For any question, feature requests or bug reports, feel free to contact me at:
# knx at aminate dot net

from distutils.core import setup
import pip

# Install pyknx if required.
try:
	import pyknx
except ImportError:
	print('Pyknx is not installed on this machine. It is going to be installed first.')
	pip.main(['install', '--pre', 'pyknx'])

# Install lxml.
try:
	import lxml
except ImportError:
	print('The lxml package is required and is not installed on this machine. If you use a GNU/Linux distribution, it is likely that its package system can provide lxml. Otherwise this script can install lxml from PyPI automatically.')
	print('If you decide to continue, lxml will be installed from PyPI. Do you want to continue? (yes/no)')
	answer = None
	while not answer:
		answer = sys.stdin.readline().lower()
		if not answer in ('yes', 'no'):
			print('Please answer either yes or no.')
			answer = None
	if answer == 'no':
		print('Installation canceled by the user.')
		exit(2)

	pip.main(['install', 'lxml'])

setup(	name='homewatcher',
		version='0.0.1b4',
		description='Alarm system built on top of Linknx',
		long_description=''.join(open('README.md').readlines()),
		author='Cyrille Defranoux',
		author_email='knx@aminate.net',
		maintainer='Cyrille Defranoux',
		maintainer_email='knx@aminate.net',
		license='GNU Public General License',
		url='https://github.com/2franix/homewatcher/',
		requires=['pyknx (>=2.0)'],
		packages=['homewatcher'],
		data_files=[('.', ['README.md'])],
		scripts=['hwconf.py', 'hwdaemon.py', 'hwresolve.py'])
