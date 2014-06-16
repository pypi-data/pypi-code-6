#!/usr/bin/env python3

import re
from .common import InfoExtractor
from ..utils import urlparse
from .auengine_io import Auengine_io_IE

class Auengine_IE(InfoExtractor):
	_VALID_URL = r'^(?:https?://)?(?:www\.)?auengine\.com/(?:.*)'
	_VALID_URL_1 = r'^(?:https?://)?(?:www\.)?auengine\.io/embed/(?:.*)'

	_PATTERN = r'url: \'(http://s[0-9]+\.auengine\.com%2F[^\s<>"]+)\''

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _dl_url(self, **kwargs):
		if re.match(self._VALID_URL_1, self.url):
			res = Auengine_io_IE(self.url,client=self.client,wpage=self.wpage)
			return  res._dl_url()
		if not re.match(self._VALID_URL, self.url): return None
		video_id = self.get_param(self.url, 'file')
		data = self._get_webpage(self.url, self.client, wpage=self.wpage)
		url = self.findall_regex(self._PATTERN, str(data['webpage']), 'auengine')
		filename = self.getFilename(url)

		return {'url': urlparse.unquote(url),
			'video_id': video_id,
			'filename': filename}
