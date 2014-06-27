#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################################################
# Author  : Jerome ODIER, Jerome FULACHIER, Fabian LAMBERT, Solveig ALBRAND
#
# Email   : jerome.odier@lpsc.in2p3.fr
#           jerome.fulachier@lpsc.in2p3.fr
#           fabian.lambert@lpsc.in2p3.fr
#           solveig.albrand@lpsc.in2p3.fr
#
#############################################################################

import os, amifs.config

#############################################################################

if __name__ == '__main__':
	#####################################################################

	try:
		from setuptools import setup

	except ImportError:
		from distutils.core import setup

	#####################################################################

	scripts = [
		'amifs_server',
	]

	if os.name == 'nt':
		scripts.append('amifs_server.bat')

	#####################################################################

	setup(
		name = 'amifs_core',
		version = amifs.config.version.encode('utf-8'),
		author = 'Jerome Odier',
		author_email = 'jerome.odier@cern.ch',
		description = 'ATLAS Metadata Interface File System (AMIFS)',
		url = 'http://ami.in2p3.fr/',
		license = 'CeCILL-C',
		packages = ['amifs'],
		package_data = {'': ['README', 'CHANGELOG', '*.txt'], 'amifs': ['*.txt']},
		scripts = scripts,
		install_requires = ['pyAMI_core'],
		zip_safe = False
	)

#############################################################################
