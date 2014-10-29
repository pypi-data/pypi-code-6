# -*- coding: utf-8 -*-
import re,sys
from pysite.compat import PORTABLE_STRING,PORTABLE_BYTES

if sys.version_info[0]==2:
	from urllib2 import unquote
elif sys.version_info[0]>=3:
	from urllib.parse import unquote

class HTTPRequestData(object):
	def __init__(self,post_values,query_string,cookies):
		if type(post_values)==PORTABLE_BYTES:
			post_values = PORTABLE_STRING(post_values,'utf-8')
		if type(query_string)==PORTABLE_BYTES:
			query_string = PORTABLE_STRING(query_string,'utf-8')
		if type(cookies)==PORTABLE_BYTES:
			cookies = PORTABLE_STRING(cookies,'utf-8')
		self.post_values = unquote(post_values.replace('+',' '))
		self.query_string = unquote(query_string.replace('+',' '))
		self.cookies = unquote(cookies.replace('+',' '))
		
	# Probe function
	@staticmethod
	def _probe_value(data,varname,defval=None):
		rx = re.compile('%s=([^&]+)' % varname)
		for match in rx.finditer(data):
			return match.group(1)
		return defval
	
	def get_post_value(self,varname,defval=None):
		return HTTPRequestData._probe_value(self.post_values,varname,defval)
	
	def get_qs_value(self,varname,defval=None):
		return HTTPRequestData._probe_value(self.query_string,varname,defval)
	
	def get_cookie_value(self,varname,defval=None):
		return HTTPRequestData._probe_value(self.cookies,varname,defval)

	def get_any_value(self,varname,defval=None):
		val = self.get_post_value(varname)
		if val==None:
			val = self.get_qs_value(varname)
		if val==None:
			val = self.get_cookie_value(varname)
		if val==None:
			return defval
		return val
