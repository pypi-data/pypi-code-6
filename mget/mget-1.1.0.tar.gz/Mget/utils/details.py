#!/usr/bin/env python3

import sys
import platform
from time import strftime, localtime
from http.client import responses
from . import (urlparse, common, write_string, report, report_error, trouble)

FILE_EXIST = "\nThe file is already fully retrieved; nothing to do.\n"

L_TIME = lambda: strftime("%a,%d %b %Y %H:%M:%S IST", localtime())
embed_url = lambda hostname: write_string("Downloading embed url form %s" % hostname)

def trying(trying, cursize, filesize):
	write_string("[%s] Read error at byte [%s/%s] - (try: %s)" % \
			(L_TIME(),cursize,filesize,trying))

def init_(url = None, **kwargs):
	site = kwargs.pop('site', None)
	cur_dl = kwargs.pop('cdl', None)
	wpage = kwargs.pop('wpage', False)
	epage = kwargs.pop('epage', False)

	if wpage or epage: string = "[%s] [%s] Downloading webpage" % (L_TIME(), site)
	elif url: string = "%s" % (urlparse.unquote(url))
	else: string = "[%s] [%s] (Download: %s)" % (L_TIME(), site, cur_dl)

	write_string(string)


def _error(msg = None, status = None):
	err = []

	if status is not None:
		err.append(status)
		err.append(responses[status])
	if msg is not None: err.append(msg)

	res = ' '.join(['%s' % s for s in err])
	string = FILE_EXIST if status == 416 else '\nERROR: %s' % (res)
	write_string(string)

def debug_info(info):
	report = []
	proxy_map = info.get('proxy') or ''
	report.append("Python Version %s %s" % (platform.python_version(),common.platform_name()))
	report.append("Proxy map %s" % {proxy_map})

	write_string("\n".join("[debug] %s" % x for x in report))

def print_info(info):
	result = []

	if info.get('quiet_mode'):
		result.append("Filesize: [%s] -> %s\n" % \
				(int(info.get('filesize')),info.get('filename')))
		write_string("\n".join(["[MGet Info] %s" % x for x in result]))
		return True

	if(info.get('proxy')): result.append("Proxy: %s" % (info.get('proxy')))

	status = info.get('status')
	b_size = info.get('filesize')
	f_size = common.format_size(b_size)

	result.append("Status code: %s %s" % (status, responses[status]))

	resume = ''
	if info.get('resuming'):
		B_size = (b_size) - int(info.get('cursize'))
		F_size = "["+common.format_size(B_size)+"]"
		resume = "%s %s" % (B_size,F_size)

	result.append("Filesize: %s [%s], %s [%s]" % (b_size,f_size,resume,info.get('type')))

	if info.get('dump_info'): result.append("FileName: %s\n" % (info.get('filename')))
	else: result.append("Saving to: %s\n" % (info['filename']))

	write_string("\n".join(["[MGet Info] %s" % x for x in result]))

def _quitting(filename, cursize, filesize):
	if cursize > filesize: filesize = cursize
	f_size = common.format_size(cursize)
	percent = "{0:.1f}%".format(common.progress(cursize,filesize))
	write_string("\n\nQuitting: ({}) {:02,} [{}]\n".format(percent,cursize,f_size))

def done_dl(speed,filename,cursize,filesize):
	if cursize > filesize: filesize = cursize
	percent = "{0:.1f}%".format(common.progress(cursize,filesize))
	string = "\n\n"+"[%s] %s at (%s) - ‘%s’ -> [%s/%s]\n" % \
			(L_TIME(),percent,speed,filename,cursize,filesize)
	write_string(string)

