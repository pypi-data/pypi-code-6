"""The file containes metadata about the distribution."""

"""Disutils package provides support for building and 
installing additional modules into Python installation.
Here the function setup is imported from the disutils 
package."""

from distutils.core import setup

"""The paramateres provided below are specific to the 
module and are self explanatory.py_modules is a list
where multiple functions which are part of the module 
can be inserted.""" 

setup (
	name		=  'checkmon',
	version 	=  '1.0.0',
	py_modules	=  ['checkmon'],
	author		=  'sree',
	author_email 	=  'sree@infomix.com',
	url		=  'http://infomix.info',
	description 	=  'Modules for server monitoring',
     )	 	
