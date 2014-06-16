#!/usr/bin/env python3

__all__ = ['std','client','common','details', 'ExtractorError',
	'DownloadError', 'ContentTooShortError', 'FormatTrace']

import os
import sys
import urllib.request as urllib
import urllib.parse as urlparse
import http.cookiejar as cookiejar

def write_string(s,newline=True,out=None):
	if out is None: out = sys.stderr
	assert type(s) == str

	if not newline and s[:1] == '\n': s = s[1:]

	out.write(s + "\n")
	out.flush()

report = lambda msg: write_string('[MGet Info] ' + str(urlparse.unquote(msg)))
report_error = lambda msg: write_string('\n[MGet Error] ' + str(urlparse.unquote(msg)))
trouble = lambda msg: write_string('\nWARNING: ' + str(urlparse.unquote(msg)))

class Default(object): pass

std = Default()
std.UA = "Mget/0.6.4 (Linux; Mac OS X; en-us)"
std.FUA = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0"
std.headers = {'Accept':'*/*', 'Accept-encoding': 'gzip,deflate'}

from .exception import *
from .handlers import *
