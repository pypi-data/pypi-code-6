#!/usr/bin/env python3

import platform
from http.client import responses
from . import (MGet, urlparse, common, write_string, _stderr, report, report_error, trouble)

FILE_EXIST = "\nThe file is already fully retrieved; nothing to do.\n"

embed_url = lambda hostname: write_string("Downloading embed url form %s" % hostname)

def init_(url = None, **kwargs):
	site = kwargs.pop('site', None)
	cur_dl = kwargs.pop('cdl', None)
	wpage = kwargs.pop('wpage', False)
	epage = kwargs.pop('epage', False)

	if wpage or epage: string = "[%s] [%s] Downloading webpage" % (MGet.get_time(), site)
	elif url: string = "[Mget Info] Location: %s" % (urlparse.unquote(url))
	else: string = "[%s] [%s] (Download: %s)" % (MGet.get_time(), site, cur_dl)

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

def get_remaining(current, total):
	B_size = total - current
	F_size = "["+common.format_size(B_size)+"]"
	return "%s %s" % (B_size,F_size)

def debug_info(info):
	report = []
	proxy_map = info.get('proxy') or ''
	report.append("Python Version %s %s" % (platform.python_version(),common.platform_name()))
	report.append("Proxy map %s" % {proxy_map})

	write_string("\n".join("[debug] %s" % x for x in report))

def print_info(info):
	resume = ''
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

	if info.get('resuming') and info.get('quit_size') == 100:
		resume = get_remaining(info.get('cursize'), b_size)

	result.append("Filesize: %s [%s], %s [%s]" % (b_size,f_size,resume,info.get('type')))
	if info.get('quit_size') != 100.0:
		e_size = int(info.get('expected'))
		e_F_size = common.format_size(info.get('expected'))
		resume = get_remaining(info.get('cursize'), e_size) if info.get('resuming') else ''
		result.append("Expecting to download: %s [%s], %s remaining" % (e_size,e_F_size,resume))

	if info.get('dump_info'): result.append("FileName: %s\n" % (info.get('filename')))
	else: result.append("Saving to: %s\n" % (info['filename']))

	write_string("\n".join(["[MGet Info] %s" % x for x in result]))

def _quitting(filename, cursize, filesize):
	if cursize > filesize: filesize = cursize
	f_size = common.format_size(cursize)
	percent = "{0:.1f}%".format(MGet.progress(float(cursize),float(filesize)))
	write_string("\n\nQuitting: ({}) {:02,} [{}]\n".format(percent,cursize,f_size))

def done_dl(speed,filename,cursize,filesize):
	if cursize > filesize: filesize = cursize
	percent = "{0:.1f}%".format(MGet.progress(float(cursize),float(filesize)))
	string = "\n\n"+"[%s] %s at (%s) - ‘%s’ -> [%s/%s]\n" % \
			(MGet.get_time(),percent,speed,filename,cursize,filesize)
	write_string(string)

