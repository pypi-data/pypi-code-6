#!/usr/bin/env python3

import re
from ..utils import urlparse
from .common import InfoExtractor

class Youtube_IE(InfoExtractor):
	_VIDEO_ID = r'^(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z-0-9]+)(?:.*)'

	DEFAULT = ['35','34','22','35','18','5']
	FORMATS = {
	'5' :'320x240 H.263/MP3 Mono FLV',
	'13':'176x144 3GP/AMR Mono 3GP',
	'17':'176x144 3GP/AAC Mono 3GP',
	'18':'480x360/480x270 H.264/AAC Stereo MP4',
	'22':'1280x720 H.264/AAC Stereo MP4',
	'34':'320x240 H.264/AAC Stereo FLV',
	'35':'640x480/640x360 H.264/AAC Stereo FLV',
	'37':'1920x1080 H.264/AAC Stereo MP4'}

	def __init__(self, url, **kwargs):
		self.url = url
		self.client = kwargs.pop('client', None)
		self.wpage = kwargs.pop('wpage', False)
		self.video_id = self.get_param(self.url, 'v')
		self.info = self.get_video_info(self.video_id)
		self._format = kwargs.pop('format', self.DEFAULT[0])

	def _extract_info(self, **kwargs):
		text = str(self.info['url_encoded_fmt_stream_map'])

		videoinfo = {
		'itag': [],
		'url': [],
		'quality': [],
		'fallback_host': [],
		's': [],
		'type': []}

		videos = text.split(',')
		videos = [video.split("&") for video in videos]

		for video in videos:
			for kv in video:
				key, value = kv.split("=")
				videoinfo.get(key, []).append(urlparse.unquote(value))

		for url in videoinfo['url']:
			if '&itag='+str(self._format) in url: url = url

		return {'url': url,
			'video_id': self.video_id}

	def get_video_info(self, id):
		url = 'http://www.youtube.com/get_video_info?&video_id=%s&el=detailpage&ps=default&eurl=&gl=US&hl=en' % id
		data = self._get_webpage(url, self.client, wpage=self.wpage)
		return urlparse.parse_qs(data['webpage'])

	def formats(self):
		self._formats = set()
		for match in re.finditer(r'itag%3D(\d+)', self.info):
			if match.group(1) not in self.FORMATS.keys(): return None
			self._formats.add(match.group(1))

		return self._formats

