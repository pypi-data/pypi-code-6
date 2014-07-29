##################################
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, GOOD TITLE or
# NON INFRINGEMENT.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
###################################

"""
Reads file with configurations and returns dictionary with sections
and options. All options will be turned into python objects (DON'T 
FORGET PUT ALL STRING OPTIONS WITHIN QUOTES).

You can use @SECTION:OPTION@ notation to refer to existed python object,
or $SECTION:OPTION$ to convert object back into a string and insert a string.

Returns option dictionary or raise an error. 
Empty dictionary indicates error with file opening, reading or parsing.

If confreader couldn't turn option into some python object, this 
options is skipped and Warning message will put in logger.

Written by Ruben Tikidji-Hamburyan <ruben.tikidji.hamburyan@gmail.com>
	with help BeetDemGuise@codereview.stackexchange.com

Date:	July 29, 2014
"""


import os
import sys
import types
import logging
from ConfigParser import ConfigParser

def is_lambda(value):
	return isinstance(value, types.LambdaType) and value.__name__ == '<lambda>'

def resolve_name(item,name_space):
	def builder(item,name_space,delimiter="@"):
		if delimiter not in item:
			return item
		result = ''
		copir = item.split(delimiter)
		#BeetDemGuise sugessted to use zip instead map 
		# (see http://codereview.stackexchange.com/questions/52729/configuration-file-with-python-functionality).
		# But zip function returns shortest argument 
		# sequence. So, the 'tail' of item after last
		# delimiter just disappiers in the result and raise
		# an error. Any ideas?
		for prefix,var in map(None,copir[::2],copir[1::2]):
			if prefix is not None: result += prefix
			if var is None: continue
			try:
				section, option = var.split(":")
			except ValueError:
				return None
			if not section in name_space : return None
			if not option in name_space[section] : return None
			if is_lambda(name_space[section][option]) or delimiter is "@":
				result += 'name_space["{}"]["{}"]'.format(section,option)
			elif delimiter is "$":
				result += str(name_space[section][option])
			else:
				return None
		return result
	# Resolve links @
	result = ''
	bld = builder(item,name_space)
	if bld is None:
		return None
	result = bld
	# Resolve strings $
	bld = builder(result,name_space,delimiter="$")
	if bld is None:
		return None
	result = bld
	return unicode(result)

def confpluspy(file_name,name_space = {},importing=None):
	"""
	Main parser.
	Parameters:
		file_name	is a name of configuration file.
		name_space	is a dictionary which will expend by new file.
		importing	is a list or tuple of line which will be executed before parsing.
					importing allows import modules which are used in configuration file.
	"""
	#importint required modules for correct parsing file
	if importing is not None:
		if type(importing) is str:
			importting = [ importing ]
		if type(importing) is not tuple or type(importing) is not list:
			raise TypeError("wrong type of import variable")
		for importline in importing:
			try:
				exec importline
			except BasexException as e:
				raise ValueError("Problem with execution of import line \'{}\':{}".format(importline,e))
	
	#check file_name
	if file_name is None:
		raise TypeError("File name is None")
	if not os.access(file_name,os.R_OK):
		raise ValueError("Cannot read file \'{}\'".format(file_name))

	#parse file
	config = ConfigParser()
	config.optionxform=str
	try:
		config.read( file_name )
	except BasexException as e:
		raise ValueError("Config Parser returns an error\'{}\'".format(e))

	#check name_space type
	if type(name_space) is not dict:
		raise TypeError("name_Space should be a dictionary")
	
	#turn all option into a Python objects
	for section in config.sections():
		if not section in name_space: name_space[section]={}
		for option in config.options(section):
			if option in name_space[section]:
				raise ValueError("Name conflict option \'{}\' exists in section [\'{}\']".format(option,section))
			xitem = unicode( config.get(section,option) )
			item = resolve_name(xitem,name_space)
			if item is None:
				raise ValueError("Problem with resolving option in  [\'%s\']\'%s\'=\'%s\'"%(section,option,xitem) ) 
			try:
				exec "name_space[\""+section+"\"][\""+option+"\"]="+item
			except :
				logging.warning("Problem with reading configuration from the %s"%file_name) 
				logging.warning("Cannot read section: \'%s\', option: \'%s\'"%(section,option) )
				logging.warning("        %s"%item)
				logging.warning("!!!! SKIPPED IT !!!!")
				pass
			
	return name_space

if __name__ == "__main__":
	cfg = cofread(sys.argv[1])
	print cfg
	for s in cfg:
		print "Section:",s
		for o in cfg[s]:
			print "     Option ",o,type(cfg[s][o])," =", cfg[s][o]
			
