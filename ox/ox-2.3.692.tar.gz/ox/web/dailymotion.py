# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
from six.moves.urllib.parse import unquote
from ox.cache import read_url


def get_video_url(url):
    '''
    >>> get_video_url('http://www.dailymotion.com/relevance/search/priere%2Bpour%2Brefuznik/video/x3opar_priere-pour-refuznik-1-jeanluc-goda_shortfilms').split('?auth')[0]
    'http://www.dailymotion.com/cdn/FLV-320x240/video/x3opar_priere-pour-refuznik-1-jean-luc-god_shortfilms.flv'

    >>> get_video_url('http://www.dailymotion.com/relevance/search/priere%2Bpour%2Brefuznik/video/x3ou94_priere-pour-refuznik-2-jeanluc-goda_shortfilms').split('?auth')[0]
    'http://www.dailymotion.com/cdn/FLV-320x240/video/x3ou94_priere-pour-refuznik-2-jean-luc-god_shortfilms.flv'
    '''
    data = read_url(url)
    video = re.compile('''video", "(.*?)"''').findall(data)
    for v in video:
       v =  unquote(v).split('@@')[0]
       return v
    return ''
