# -*- coding: utf-8 -*-
import oembed


ENDPOINTS = {
    'youtube': oembed.OEmbedEndpoint('http://www.youtube.com/oembed', [
        'https?://(*.)?youtube.com/*',
        'https?://youtu.be/*',
        '//(*.)?youtube.com/*',
        '//youtu.be/*'
    ]),
    'flickr': oembed.OEmbedEndpoint('http://www.flickr.com/services/oembed/', [
        'https?://*.flickr.com/*',
        '//*.flickr.com/*',
    ]),
    'vimeo': oembed.OEmbedEndpoint('http://vimeo.com/api/oembed.json', [
        'https?://vimeo.com/*',
        '//vimeo.com/*',
    ]),
}
