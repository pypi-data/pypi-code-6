#!/usr/bin/env python3

import re
import os
import sys
import zlib
import lxml.html
from io import StringIO
from . import strip_site
from ..utils import (client, details, urlparse)

class InfoExtractor(object):
	@staticmethod
	def _get_webpage(url, client, **kwargs):
		site = strip_site(url)
		wpage = kwargs.pop('wpage', False)
		Req_head = kwargs.pop('Req_head', {})

		urllibObj, req = client.urlopen(url,req_head=Req_head)
		webpage = urllibObj.read().decode('utf-8')
		if wpage:
			filename = site[0] + '.dump'
			with open(filename, 'w') as f:
				f.write(webpage)
				details.report("Webpage writtern to %s" % filename)
		
		return {'webpage': webpage,
			'urllibObj': urllibObj,
			'request': req}

	@staticmethod
	def search_regex(pattern, string, name, flags=0):
		mObj = re.search(pattern, string, flags)
		if mObj: return next(s for s in mObj.groups() if s is not None)
		return None

	@staticmethod
	def findall_regex(pattern, string, name):
		mObj = re.findall(pattern, string)
		if mObj: return next(s for s in mObj if s is not None)
		return None

	@staticmethod
	def get_param(url, param):
		query = urlparse.urlparse(url).query
		query = query.split('&')
		for i in query:
			if i.startswith(str(param + '=')): return i.split('=')[1]
		return None

	@staticmethod
	def getFilename(url):
		url = urlparse.unquote(url)
		filename = os.path.basename(urlparse.urlparse(url).path)
		if len(filename.strip(" \n\t.")) == 0: return None
		return urlparse.unquote_plus(filename)

	@staticmethod
	def get_embed_url(url, client, wpage):
		data = InfoExtractor._get_webpage(url, client, wpage=wpage)
		htmltree = lxml.html.fromstring(str(data['webpage']))

		src = None
		for frame in htmltree.xpath('//iframe'):
			src = frame.attrib['src']
		if src is None:
			for frame in htmltree.xpath('//embed'):
				src = frame.attrib['src']
		return src
