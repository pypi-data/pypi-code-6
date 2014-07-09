#!/usr/bin/env python3

import os, sys
import time
from ..utils import common, urlparse

class FileDownloader(object):
	def __init__(self, info = {}):
		self.params = info
		self.last_len = 0

	@staticmethod
	def getLocalFilesize(filename):
		if not os.path.exists(filename): return None
		return os.path.getsize(os.path.join('.', filename))

	def _progress_bar(self, s_dif = None, progress = None, bytes = None, dif = None, width = 46):
		term_width = common.get_term_width()
		width = term_width - width

		data_len = (self.cursize - self.resume_len)

		_res = ["%-6s" % ("{0:.1f}%".format(float(progress) * 100.0)),
			"[" + "="*int(progress*width)+">" + " "*(width-int(progress*width)) + "] ",
			"%-12s " % ("{:02,}".format(self.cursize,self.filesize)),
			"%9s " % (self.calc_speed(dif,bytes)),
			"eta "+self.calc_eta(s_dif,bytes,data_len,self.remaining)]

		line = "".join(["%s" % x for x in _res])
		if self.params.get('newline'): sys.stdout.write('\n')
		else:sys.stdout.write('\r')
		if self.last_len: sys.stdout.write('\b' * self.last_len)

		sys.stderr.write("\r")
		sys.stdout.write(line)
		sys.stdout.flush()
		self.last_len = len(line)

	def get_progress(self):
		progress = float(self.cursize)/float(self.filesize)
		if progress < 0: progress = 0
		if progress > 1: progress = 1
		return progress

	def calc_speed(self, dif, bytes):
		if bytes == 0 or dif < 0.001: return "%9s" % ("--.-K/s")
		return "%s" % ('%s/s' % (common.format_size(float(bytes) / dif)))

	def calc_eta(self, dif, bytes, current, total):
		if current == 0 or dif < 0.001: return '--:--'
		rate = float(current) / dif
		eta = int((float(total) - float(current)) / rate)
		return common.format_time(eta)

