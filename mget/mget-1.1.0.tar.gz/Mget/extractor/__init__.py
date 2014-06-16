#!/usr/bin/env python3

__all__ = ['strip_site']

import re
from ..utils import (std, common, details, urlparse, ExtractorError)

def strip_site(url):
	url = urlparse.urlparse(url).hostname
	hostname = re.match(r'(?:\w*://)?(?:.*\.)?([a-z-A-Z-0-9]*\.([a-z]*))', url).groups()[0]
	site = hostname.split('.')[0]
	return hostname, site

from .common import InfoExtractor
from .anivids import Anivids_IE
from .aniupload import Aniupload_IE
from .auengine import Auengine_IE
from .mp4upload import Mp4upload_IE
from .playpanda import Playpanda_IE
from .trollvid import Trollvid_IE
from .videonest import Videonest_IE
from .videodrive import Videodrive_IE
from .yourupload import Yourupload_IE
from .youtube import Youtube_IE

_SITE_LIST = [	'mp4upload.com', 'trollvid.net', 'anivids.tv', 'auengine.com', 'auengine.io',
		'aniupload.com', 'yourupload.com', 'youtube.com', 'videonest.net', 'videodrive.tv',
		'playpanda.net']
_ALL_CLASSES = [klass for name, klass in globals().items() if name.endswith('_IE')]

def gen_extractors():
	return [klass() for klass in _ALL_CLASSES]

def get_info_extractor(ie_name):
	return globals()[ie_name.capitalize()+'_IE']

def get_info(url, client, info):
	newurl = None; result = {}
	hostname, site = strip_site(url)
	ret = {	'url': url,
		'site': site,
		'hostname': hostname,
		'filename': InfoExtractor.getFilename(url)}
	if info.get('mirror'): return ret

	wpage = info.get('wpage')
	details.init_(site=site,cdl=info.get('cur_download',1),wpage=wpage,epage=info.get('embedurl'))

	if hostname in ('animeram.eu','animewaffles.tv','cc-anime.com'):
		try: newurl = InfoExtractor.get_embed_url(url,client=client,wpage=wpage)
		except: raise ExtractorError("Unable to extract: %s" % hostname)

	if newurl is not None:
		hostname, site = strip_site(newurl)
		ret['eurl'] = newurl
		ret['hostname'] = hostname

	if info.get('embedurl'): return ret

	format = info.get('v_format')
	if hostname in _SITE_LIST:
		ie = get_info_extractor(site)
		try:
			res = ie(ret.get('url'),client=client,wpage=wpage,format=format)
			result = res._dl_url()
		except: raise ExtractorError("Unable to extract: %s" % hostname)

	if result is None or result.get('url') is None: return ret

	result['hostname'] = ret.get('hostname')
	return result

