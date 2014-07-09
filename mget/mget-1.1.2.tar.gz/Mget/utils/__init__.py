#!/usr/bin/env python3

__all__ = ['strip_site','std','client','common','details','MGet','ExtractorError',
	'DownloadError', 'ContentTooShortError', 'FormatTrace']

import re
import urllib.request as urllib
import urllib.parse as urlparse
import http.cookiejar as cookiejar
from html.parser import HTMLParser

from .mgetsys import MGet

_SITE_LIST = [	'mp4upload.com', 'trollvid.net', 'anivids.tv', 'auengine.com', 'auengine.io',
		'aniupload.com', 'yourupload.com', 'youtube.com', 'videonest.net', 'videodrive.tv',
		'playpanda.net', 'video44.net', 'play44.net', 'bzoo.org']

def write_string(s,newline=True):
	assert type(s) == str

	if not newline and s[:1] == '\n': s = s[1:]
	MGet.write_string(s.encode('utf-8'))

def strip_site(url):
	url = urlparse.urlparse(url).hostname
	hostname = re.match(r'(?:\w*://)?(?:.*\.)?([a-z-A-Z-0-9]*\.([a-z]*))', url).groups()[0]
	site = hostname.split('.')[0]
	return hostname, site

_stderr = lambda msg: write_string('\n' + str(urlparse.unquote(str(msg))))
report = lambda msg: write_string('[MGet Info] ' + str(urlparse.unquote(str(msg))))
report_error = lambda msg: write_string('\n[MGet Error] ' + str(urlparse.unquote(str(msg))))
trouble = lambda msg: write_string('\nWARNING: ' + str(urlparse.unquote(str(msg))))

class Default(object): pass

std = Default()
std.UA = "Mget/0.6.4 (Linux; Mac OS X; en-us)"
std.FUA = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0"
std.headers = {	'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}
std.site_list = _SITE_LIST
std.share_site_list = [ 'animeram.eu','animewaffles.tv','cc-anime.com']

from .exception import *
from .handlers import *
