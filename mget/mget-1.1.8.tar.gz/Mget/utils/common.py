#!/usr/bin/env python3

import os, sys
import locale
import platform
import traceback
from http.client import responses
from . import (MGet, urlparse, write_string, _stderr, report, report_error, trouble, HTMLParser)

FILE_EXIST = "\nThe file is already fully retrieved; nothing to do.\n"

def _error(msg = "", status = 0): MGet._error(str(msg).encode(), status)
def get_term_width(): return MGet._term_width()

def pref_encoding():
	try: pref = locale.getpreferredencoding(); u'MGet'.encode(pref)
	except: pref = 'UTF-8'
	return pref

def FormatTrace(exc_info):
	ex_type, ex_value, tb = exc_info
	tb = traceback.extract_tb(tb)[0]

	etype = ex_type.__name__
	emodule = ex_type.__module__

	if emodule not in ('__main__', 'builtins'):
		etype = etype + '.' + emodule

	r = ["File: %s, line %s, <module> %s" % (tb[0],tb[1],tb[2])]
	r.append("With: %s" % tb[3])
	r.append("%s: %s"% (etype,ex_value))

	return ''.join("[debug] %s\n" % x for x in r)

def platform_name():
	result = platform.platform()
	if isinstance(result, bytes):
		result = result.decode(pref_encoding())

	assert isinstance(result, str)
	return result

def EXFilename(filename):
	idx = 1
	dirname = '.'

	name, ext = filename.rsplit('.', 1)
	names = [x for x in os.listdir(dirname) if x.startswith(name)]
	names = [x.rsplit('.', 1)[0] for x in names]
	suffixes = [x.replace(name, '') for x in names]

	suffixes = [x[2:-1] for x in suffixes if x.startswith('-(') and x.endswith(')')]
	indexes  = [int(x) for x in suffixes if set(x) <= set('0123456789')]
	if indexes: idx += sorted(indexes)[-1]
	return ('%s-(%d).%s' % (name, idx, ext))

def debug_info(info):
	report = []
	proxy_map = info.get('proxy') or ''
	report.append("Python Version %s %s" % (platform.python_version(),platform_name()))
	report.append("Proxy map %s" % {proxy_map})

	write_string("\n".join("[debug] %s" % x for x in report))

def write_info(info):
	result = []

	result.append("\n".join("%s" % x for x in info.get('report')))
	result.append("Python Version %s %s\n" % (platform.python_version(),platform_name()))
	result.append("Default Url\t: %s" % info.get('defurl'))
	result.append("Url\t\t: %s" % info.get('url'))
	result.append("Proxy\t\t: %s" % ({} if info.get('proxy') == None else info.get('proxy')))
	result.append("Status\t\t: %s" % info.get('status'))
	result.append("Type\t\t: %s" % info.get('type'))
	result.append("Filename\t: %s" % info.get('filename'))
	result.append("Filesize\t: %s" % info.get('filesize'))
	result.append("Headers\t\t: %s" % (dict(info.get('headers'))))

	data = "\n".join("%10s" % x for x in result)

	log_filename = info.get('log_file')
	if os.path.exists(log_filename): log_filename = EXFilename(log_filename)
	with open(log_filename, 'w') as f:
		f.write(data)
		report('Done Writting information to %s\n' % info.get('log_file'))
	return True

class MyHTMLParser(HTMLParser):
	def __init__(self, html, tag = {}, hostname = None):
		HTMLParser.__init__(self)
		self.data = {}
		self.start_tag = tag
		self.hostname = hostname
		self.html = html

	def load(self):
		self.feed(self.html)
		self.close()

	def handle_starttag(self, tag, attrs):
		if tag not in self.start_tag: return 
		for name, value in attrs:
			if name in self.name or value in self.value:
				self.data[self.hostname] = value

	def get_result(self, tag, name=None, value=None):
		self.start_tag = tag
		self.name = name or ''
		self.value = value or ''
		self.load()
		if self.hostname in self.data:
			return self.data[self.hostname]
		else: return

