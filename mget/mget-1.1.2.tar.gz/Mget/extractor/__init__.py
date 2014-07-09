#!/usr/bin/env python3

from ..utils import (strip_site, std, common, details, urlparse, ExtractorError)
from .common import InfoExtractor
from .anivids import Anivids_IE
from .aniupload import Aniupload_IE
from .auengine import Auengine_IE
from .mp4upload import Mp4upload_IE
from .playpanda import Playpanda_IE
from .play44 import Play44_IE
from .trollvid import Trollvid_IE
from .videonest import Videonest_IE
from .videodrive import Videodrive_IE
from .yourupload import Yourupload_IE
from .youtube import Youtube_IE

_ALL_CLASSES = [klass for name, klass in globals().items() if name.endswith('_IE')]

def get_info_extractor(ie_name):
	return globals()[ie_name.capitalize()+'_IE']

def get_info(url, client, info):
	newurl = None; result = {}
	hostname, site = strip_site(url)
	ret = {	'url': url,
		'site': site,
		'hostname': hostname,
		'filename': InfoExtractor.getFilename(url)}

	wpage = info.get('wpage')
	details.init_(site=site,cdl=info.get('cur_download',1),wpage=wpage,epage=info.get('embedurl'))

	if info.get('mirror'): return ret
	if hostname in ('animeram.eu','animewaffles.tv','cc-anime.com'):
		try: newurl = InfoExtractor.get_embed_url(url,client=client,wpage=wpage)
		except: raise ExtractorError("unable to find embed url in: %s" % hostname)

	if newurl is not None:
		hostname, site = strip_site(newurl)
		if not info.get('embedurl'): details.report("Embed url: %s" % newurl)
		ret['url'] = newurl
		ret['hostname'] = hostname

	if info.get('embedurl'): return ret

	hostname, site = strip_site(ret.get('url'))
	format = info.get('v_format')
	if hostname in std.site_list:
		try:
			ie = get_info_extractor(site)
			res = ie(ret.get('url'),client=client,wpage=wpage,format=format)
		except: raise ExtractorError("Unable to Extract : %s " % hostname)
		result = res._extract_info()

	if result is None or result.get('url') is None: return ret

	result['hostname'] = ret.get('hostname')
	return result

