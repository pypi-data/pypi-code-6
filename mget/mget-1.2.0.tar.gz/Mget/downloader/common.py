#!/usr/bin/env python3

import os, sys
import time
from ..utils import (std, strip_site, MGet, urlparse, HTMLParser)

class FileDownloader(MGet):
	def __init__(self, info = {}):
		self.params = info
		self.last_len = 0

	@staticmethod
	def getLocalFilesize(filename):
		if not os.path.exists(filename): return None
		return os.path.getsize(os.path.join('.', filename))

	def _progress_bar(self, s_dif = None, progress = None, bytes = None, dif = None, width = 46):
		width = self._term_width() - width
		data_len = (self.cursize - self.resume_len)

		quit_size = (self.quit_size / 100.0)
		if progress > quit_size: quit_size = progress

		prog = int(progress * width)
		prog_bal = width - int(progress * width)

		if self.quit_size != 100.0:
			expect = int(quit_size * width)
			ex_bal = int((width - expect) - 2)
			ex_prog_bal = int(expect - int(progress * width))
			progress_bar = "["+"="*(prog)+">"+" "*(ex_prog_bal)+"]["+" "*(ex_bal)+"] "
		else:
			progress_bar = "["+"="*(prog)+">"+" "*(prog_bal)+"] "

		_res = ["%-6s" % ("{0:.1f}%".format(float(progress) * 100.0)), progress_bar,
			"%-12s " % ("{:02,}".format(self.cursize)),
			"%9s " % (self.calc_speed(dif,bytes).decode()),
			"eta "+ self.calc_eta(s_dif, bytes, data_len, self.remaining).decode()]

		line = "".join(["%s" % x for x in _res])
		if self.params.get('newline'): sys.stdout.write('\n')
		else:sys.stdout.write('\r')
		if self.last_len: sys.stdout.write('\b' * self.last_len)

		sys.stdout.write("\r")
		sys.stdout.write(line)
		sys.stdout.flush()
		self.last_len = len(line)

	def _progress(self): return self.get_progress(self.cursize, self.filesize)

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
				hostname, site = strip_site(value)
				if hostname in std.site_list:
					self.data[self.hostname] = value

	def get_result(self, tag, name=None, value=None):
		self.start_tag = tag
		self.name = name or ''
		self.value = value or ''
		self.load()
		if self.hostname in self.data:
			return self.data[self.hostname]
		else: return

