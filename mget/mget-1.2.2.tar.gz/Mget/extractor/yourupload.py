#!/usr/bin/env python3

import re
from .common import InfoExtractor

class Yourupload_IE(InfoExtractor):
	_VALID_URL = r'^(?:https?://)?yourupload\.com/embed/(?:.*)'
	_VIDEO_ID = r'^(?:https?://)?([^\s<>"])?yourupload\.com/embed/([a-z-A-Z-0-9]+)'

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _extract_info(self, **kwargs):
		if not re.match(self._VALID_URL, self.url): return None
		video_id = self.search_regex(self._VIDEO_ID, self.url, 'yourupload')
		data = self._get_webpage(self.url,self.client,wpage=self.wpage)
		url = self.findall_regex(r'file: "(.+?)"', str(data['webpage']), 'yourupload')

		return {'url': url,
			'filename': self.getFilename(url)}
