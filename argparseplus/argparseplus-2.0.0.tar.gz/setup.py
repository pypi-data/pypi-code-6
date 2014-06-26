#!/usr/bin/env python

#############################################################################
# Author  : Jerome ODIER
#
# Email   : jerome.odier@cern.ch
#
#############################################################################

VERSION = '2.0.0'

#############################################################################

try:
	from setuptools import setup

except ImportError:
	from distutils.core import setup

#############################################################################

setup(
	name = 'argparseplus',
	version = VERSION,
	author = 'Jerome Odier',
	author_email = 'jerome.odier@cern.ch',
	description = 'argparse extensions.',
	url = 'https://bitbucket.org/jodier/argparseplus',
	license = 'CeCILL-C',
	packages = ['argparseplus'],
)

#############################################################################
