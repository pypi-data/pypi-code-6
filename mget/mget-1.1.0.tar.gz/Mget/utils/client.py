#!/usr/bin/env python3

import os
import ssl
import socket
from . import (urllib, urlparse, cookiejar, details, RedirectHandler, MGetDLHandler)

class Client(object):
	def __init__(self, proxy = None,info = {}):
		self.info = info
		self.proxy = self.info.get('proxy')
		self.cookiefile = self.info.get('cookiefile')
		self.timeout = self.info.get('timeout')

		self._setup_opener()

	def getInfos(self, url, cursize):
		(urlObj, request) = self.urlopen(url,cursize,req_head={'no-encoding':'True'})
		if urlObj is None: return None
		headers = urlObj.info()

		return {'url': url,
			'headers': headers,
			'urllibObj': urlObj,
			'request': request,
			'cookiejar': self.cookiejar,
			'status': urlObj.getcode(),
			'filesize': self.getFilesize(headers),
			'type': headers.get('content-type') or 'unknown'}

	def urlopen(self, url, cursize = 0, req_head = None, params = None):
		getType = lambda url: urlparse.urlparse(url).scheme
		headers = {'User-Agent':self.info.get('user-agent')}

		if req_head: headers.update(req_head)
		if self.info.get('dump_ua'): details.report('User-Agent: '+headers.get('User-Agent'))
		if cursize != 0: headers['Range'] = 'bytes=%s-' % (cursize)
		if params: params = urlparse.urlencode(params).encode('utf-8')

		request = urllib.Request(urllib.unquote(url),headers=headers)

		try:urllibObj = self.opener.open(request, params)
		except urllib.HTTPError as e: details._error(status=e.code); return self.EXHandle()
		except urllib.URLError as e: details._error(e.reason); return self.EXHandle()
		except (socket.error, socket.timeout) as e: details._error(e); return self.EXHandle()

		return urllibObj, request

	def EXHandle(self):
		if self.info.get('ignore'): return (None, None)
		else: exit(1)

	def getFilesize(self, headers):
		if 'content-range' in headers: filesize = headers.get('content-range').split('/')[1]
		else: filesize = headers.get('content-length')
		return int(filesize)

	def _setup_opener(self):
		if self.cookiefile is None: self.cookiejar = cookiejar.CookieJar()
		else:
			self.cookiejar = cookiejar.MozillaCookieJar(self.cookiefile)
			if os.access(self.cookiefile, os.R_OK): self.cookiejar.load()

		cookie_processor = urllib.HTTPCookieProcessor(self.cookiejar)
		if self.proxy: 
			if self.proxy == '': proxies = {}
			else: proxies = {'http':self.proxy,'https':self.proxy}
		else:
			proxies = urllib.getproxies()
			if 'http' in proxies and 'https' not in proxies:
				proxies['https'] = proxies['http']

		proxy_handler = urllib.ProxyHandler(proxies)
		https_handler = self.HTTPSHandler(no_check = True, debuglevel=0)
		self.opener = urllib.build_opener(MGetDLHandler, RedirectHandler, https_handler,
						proxy_handler, cookie_processor)
		self.opener.addheaders = []
		urllib.install_opener(self.opener)
		socket.setdefaulttimeout(self.timeout)

	def HTTPSHandler(self, no_check, **kwargs):
		context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
		context.verify_mode = (ssl.CERT_NONE if no_check else ssl.CERT_REQUIRED)
		context.set_default_verify_paths()
		try:context.load_default_certs()
		except:pass

		return urllib.HTTPSHandler(context=context, **kwargs)

