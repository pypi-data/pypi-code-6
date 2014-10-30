#!/usr/bin/python
# -*- coding: utf-8 -*-

from pysite.subhandlers import BaseHandler

class DownloadHandler(BaseHandler):
	
	def __init__(self,*args,**kw):
		BaseHandler.__init__(self,*args,**kw)
		self.response_headers.append( ('Content-Type','application/octet-stream') )

	def filename(self):
		"""
		Re-implement to return the filename that should be used as download filename
		"""
		raise NotImplementedError

	def filepath(self):
		"""
		The path of the file to be sent
		"""
		raise NotImplementedError

	def chunksize(self):
		"""
		Specify a chunk-size in bytes. The chunk-size controls how much memory will be allocated during the download streaming.
		Low size: means low memory-consumption, but many block-reads, High size the opposite.
		"""
		return 1024
	
	def init(self):
		self.template_info['template_off'] = True
		self.response_headers.append( ('Content-Disposition','attachment; filename="%s"' % self.filename() ) )
		f = open(self.filepath(),'rb')
		return iter(lambda: f.read(self.chunksize()), '')
