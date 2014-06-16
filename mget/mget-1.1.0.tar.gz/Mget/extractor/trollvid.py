#!/usr/bin/env python3

import re
from .common import InfoExtractor
from ..utils import std

class Trollvid_IE(InfoExtractor):
	_VALID_URL = r'^(?:https?://)?[^\s<>"]+|www\.trollvid\.net/(?:.*)'

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _dl_url(self, **kwargs):
		if not re.match(self._VALID_URL, url): return None
		video_id = self.get_param(url, 'file')
		data = self._get_webpage(self.url, self.client,\
				Req_head = {'User-Agent':std.FUA}, wpage=self.wpage)
		url = self.findall_regex(r'http%3A%2F%2F[^\s<>"]+', str(data), 'trollvid')

		urllibObj, req = client.urlopen(url)
		url = urllibObj.geturl()

		name, ext = self.getFilename(url).split('.')
		filename = "%s-%s.%s" % (name,video_id,ext)

		return {'url': url,
			'filename': filename}
