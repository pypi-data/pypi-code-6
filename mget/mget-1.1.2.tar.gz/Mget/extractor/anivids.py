#!/usr/bin/env python3

import re
from .common import InfoExtractor

class Anivids_IE(InfoExtractor):
	_VALID_URL =  r'^(?:https?://)?(?:www\.)?anivids\.tv/(?:.*)'
	_VIDEO_ID = r'^(?:https?://)?(?:www\.)?anivids\.tv/embed-([a-z-A-Z-0-9]+)'


	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)

	def _extract_info(self, **kwargs):
		if not re.match(self._VALID_URL, self.url): return None
		video_id = self.search_regex(self._VIDEO_ID, self.url, 'anivids')
		data = self._get_webpage(self.url, self.client, wpage=self.wpage)
		d = self.search_regex('67,(.+?).split', str(data['webpage']), 'anivids')
		r = (d.split('|')[2:])

		ip = "%s.%s.%s.%s" %  (r[18],r[17],r[15],r[14])
		port = "%s" %  (r[13])
		key = "%s" % (r[25])

		url = "http://%s:%s/%s/%s" % (ip,port,key,'v.'+r[24])

		name,ext = self.getFilename(url).split('.')
		filename = "%s-%s.%s" % (name,video_id,ext)

		return {'url': "http://%s:%s/%s/%s" % (ip,port,key,filename),
			'filename': filename}
