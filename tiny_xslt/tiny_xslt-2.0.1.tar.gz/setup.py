#!/usr/bin/env python

#############################################################################
# Author  : Jerome ODIER
#
# Email   : jerome.odier@cern.ch
#
#############################################################################

VERSION = '2.0.1'

#############################################################################

try:
	from setuptools import setup

except ImportError:
	from distutils.core import setup

#############################################################################

setup(
	name = 'tiny_xslt',
	version = VERSION,
	author = 'Jerome Odier',
	author_email = 'jerome.odier@cern.ch',
	description = 'Easy XSL transformations.',
	url = 'https://bitbucket.org/jodier/tiny_xslt',
	download_url = 'https://pypi.python.org/packages/source/t/tiny_xslt/tiny_xslt-' + VERSION + '.tar.gz',
	license = 'CeCILL-C',
	packages = ['tiny_xslt'],
)

#############################################################################
