#!/usr/bin/env python3

import os, sys
import locale
import platform
import  traceback
from math import log
from . import (urlparse, MGet, report, report_error, trouble, HTMLParser, _SITE_LIST)

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

def pref_encoding():
	try: pref = locale.getpreferredencoding(); u'TEST'.encode(pref)
	except: pref = 'UTF-8'
	return pref

def format_size(bytes):
	bytes = int(bytes)
	UNITS = [('B', 0), ('K', 2), ('M', 2)]

	if bytes > 1:
		exponent = min(int(log(bytes, 1024.0)), len(UNITS)-1)
		quotient = float(bytes) / float(1024 ** exponent)
		(unit, decimals) = UNITS[exponent]
		result = "{:.%sf}{}" % (decimals)

		return result.format(quotient, unit)

	else: return 'Unknown'

def format_time(duration):
	(mins, secs) = divmod(duration, 60)
	(hours, mins) = divmod(mins, 60)
	if hours > 99: ret = '--:--'
	elif hours == 0 and mins == 0:
		ret = '%02ds' % (secs) if secs >= 10 else '%2ds' % (secs)
	elif hours == 0: ret = '%02dm %02ds' % (mins, secs)
	else: ret = '%02dh %02dm' % (hours, mins)

	return "%07s" % ret

def best_block_size(est_time, bytes):
	new_min = max(bytes / 2.0, 1.0)
	new_max = min(max(bytes * 2.0, 1.0), 4194304)

	if est_time < 0.001: return int(new_max)

	rate = bytes / est_time

	if rate > new_max: return int(new_max)
	if rate < new_min: return int(new_min)

	return int(rate)

def platform_name():
	result = platform.platform()
	if isinstance(result, bytes):
		result = result.decode(pref_encoding())

	assert isinstance(result, str)
	return result


def get_term_width():
	if sys.version_info >= (3,3):
		return os.get_terminal_size().columns
	columns = os.environ.get('COLUMNS', None)
	if columns: return int(columns)

	import subprocess
	try:
		sp = subprocess.Popen( ['stty', 'size'],
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = sp.communicate()
		return int(out.split()[1])
	except: pass
	return None

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

