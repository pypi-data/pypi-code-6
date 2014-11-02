# -*- coding: utf-8 -*-
import re,sys
from pysite.compat import PORTABLE_STRING,PORTABLE_BYTES
from pysite.conf import getConfiguration
from pysite.tools.log import logger,get_traceback

if sys.version_info[0]==2:
	from urllib2 import unquote
elif sys.version_info[0]>=3:
	from urllib.parse import unquote

class HTTPRequestData(object):
	def __init__(self,post_values,query_string,cookies):
		self.log = logger(getConfiguration())
		if type(post_values)==PORTABLE_BYTES:
			post_values = PORTABLE_STRING(post_values,'utf-8')
		if type(query_string)==PORTABLE_BYTES:
			query_string = PORTABLE_STRING(query_string,'utf-8')
		if type(cookies)==PORTABLE_BYTES:
			cookies = PORTABLE_STRING(cookies,'utf-8')
		self.post_values = {}
		self.query_string = {}
		self.cookies = {}
		if post_values:
			try:
				self.post_values = dict(map(lambda v: unquote(v.replace('+',' ')).split('='), post_values.split('&')))
			except:
				self.log.error('post values have bad syntax')
		if query_string:
			try:
				self.query_string = dict(map(lambda v: unquote(v.replace('+',' ')).split('='), query_string.split('&')))
			except:
				self.log.error('post values have bad syntax')
		if cookies:
			try:
				self.cookies = dict(map(lambda v: unquote(v.replace('+',' ')).split('='), cookies.split('; ')))
			except:
				self.log.error('post values have bad syntax')
		
	def get_post_value(self,varname,defval=None):
		return self.post_values.get(varname,defval)
	
	def get_qs_value(self,varname,defval=None):
		return self.query_string.get(varname,defval)
	
	def get_cookie_value(self,varname,defval=None):
		return self.cookies.get(varname,defval)

	def get_any_value(self,varname,defval=None):
		val = self.get_post_value(varname)
		if val==None:
			val = self.get_qs_value(varname)
		if val==None:
			val = self.get_cookie_value(varname)
		if val==None:
			return defval
		return val
