# -*- coding: utf-8 -*-
# ci:si:et:sw=4:sts=4:ts=4
import re

from . import cache
from .text import find_re
from .utils import json, ET

def get_embed_code(url, maxwidth=None, maxheight=None):
    embed = {}
    header = cache.get_headers(url)
    if header.get('content-type', '').startswith('text/html'):
        html = cache.read_url(url)
        json_oembed = filter(lambda l: 'json+oembed' in l, re.compile('<link.*?>').findall(html))
        xml_oembed = filter(lambda l: 'xml+oembed' in l, re.compile('<link.*?>').findall(html))
        if json_oembed:
            oembed_url = find_re(json_oembed[0], 'href="(.*?)"')
            if maxwidth:
                oembed_url += '&maxwidth=%d' % maxwidth
            if maxheight:
                oembed_url += '&maxheight=%d' % maxheight
            embed = json.loads(cache.read_url(oembed_url))
        elif xml_oembed:
            oembed_url = find_re(json_oembed[0], 'href="(.*?)"')
            if maxwidth:
                oembed_url += '&maxwidth=%d' % maxwidth
            if maxheight:
                oembed_url += '&maxheight=%d' % maxheight
            data = cache.read_url(oembed_url)
            for e in ET.fromstring(data):
                embed[e.tag] = e.text
    return embed
