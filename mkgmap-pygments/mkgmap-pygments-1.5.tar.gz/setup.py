#!/usr/bin/env python

from os import path
from codecs import open
from setuptools import setup

# Get the long description
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
	long_description = f.read()

setup(name='mkgmap-pygments',
	version='1.5',
	description='A pygments lexer and style for mkgmap style files',
	long_description=long_description,
	keywords='mkgmap syntax highlighting',
	author='Steve Ratcliffe',
	author_email='sr@parabola.me.uk',
	url='https://bitbucket.org/sratcliffe/mkgmap-pygments',
	license='GPLv3+',
	platforms='any',

	classifiers=[
		'Development Status :: 5 - Production/Stable',

		'Intended Audience :: Developers',
		'Intended Audience :: End Users/Desktop',

		# Pick your license as you wish (should match "license" above)
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

		# Specify the Python versions you support here. In particular, ensure
		# that you indicate whether you support Python 2, Python 3 or both.
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',

		'Topic :: Text Processing :: Filters',
	],

	packages=['mkgmap'],

	entry_points={
		'pygments.lexers': ['mkgmap = mkgmap.mkgmap_lex:MkgmapLexer'],
		'pygments.styles': ['mkgmap = mkgmap.mkgmap_style:MkgmapStyle'],
	},

	install_requires = ['Pygments'],
)
