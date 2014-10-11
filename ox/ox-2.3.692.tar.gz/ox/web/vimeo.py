# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

import json

from ox.cache import read_url


def get_data(id):
    url = 'http://vimeo.com/api/v2/video/%s.json' % id
    data = json.loads(read_url(url).decode('utf-8'))[0]

    url = 'http://player.vimeo.com/video/%s/config?autoplay=0&byline=0&bypass_privacy=1&context=clip.main&default_to_hd=1&portrait=0' % id    
    info = json.loads(read_url(url).decode('utf-8'))
    data['video'] = info['request']['files']['h264']
    return data

