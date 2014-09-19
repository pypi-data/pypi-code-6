#!/usr/bin/env python3

import re
from .common import InfoExtractor

class Yourupload_IE(InfoExtractor):
	VALID_URL1 = r'^(?:https?://)?yourupload\.com/embed/(?:.*)'
	VALID_URL2 = r'^(?:https?://)?embed\.yourupload\.com/(?:.*)'
	_VIDEO_ID = r'^(?:https?://)?([^\s<>"])?yourupload\.com/embed/([a-z-A-Z-0-9]+)'

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _extract_info(self, **kwargs):
		if not re.match(self.VALID_URL1,self.url) and not re.match(self.VALID_URL2,self.url):
			return None

		video_id = self.search_regex(self._VIDEO_ID, self.url, 'yourupload')
		data = self._get_webpage(self.url,self.client,wpage=self.wpage)
		url = self.findall_regex(r'file: "(.+?)"', str(data['webpage']), 'yourupload')

		return {'url': url,
			'filename': self.getFilename(url)}
