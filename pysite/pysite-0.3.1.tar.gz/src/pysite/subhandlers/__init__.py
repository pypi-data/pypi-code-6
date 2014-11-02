#!/usr/bin/python
# -*- coding: utf-8 -*-

class BaseHandler(object):
	
	def __init__(self,*args,**kw):
		self.template_info = args[0]
		self.response_headers = args[1]
		self.environ = args[2]
		self.translate = args[3]
		self.req_data = args[4]
