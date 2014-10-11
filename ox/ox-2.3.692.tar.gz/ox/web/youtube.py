# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from six.moves.urllib.parse import quote, unquote_plus
from six.moves import urllib
from six.moves import http_cookiejar as cookielib
import re
from xml.dom.minidom import parseString
import json

import feedparser
import ox
from ox.cache import read_url, cache_timeout


def get_id(url):
    match = re.compile('v=(.+?)($|&)').findall(url)
    if match:
        return match[0][0]

def get_url(id):
    return 'http://www.youtube.com/watch?v=%s' % id

def video_url(youtubeId, format='mp4', timeout=cache_timeout):
    """
        youtubeId - if of video
        format - video format, options: webm, 1080p, 720p, mp4, high
    """
    fmt = None
    if format == '4k':
        fmt=38
    elif format == '1080p':
        fmt=37
    elif format == '720p':
        fmt=22
    elif format == 'mp4':
        fmt=18
    elif format == 'high':
        fmt=35
    elif format == 'webm':
        streams = videos(youtubeId, 'webm')
        return streams[max(streams.keys())]['url']

    streams = videos(youtubeId)
    if str(fmt) in streams:
        return streams[str(fmt)]['url']

def get_video_info(id):
    eurl = get_url(id)
    data = read_url(eurl)
    t = re.compile('\W[\'"]?t[\'"]?: ?[\'"](.+?)[\'"]').findall(data)
    if t:
        t = t[0]
    else:
        raise IOError
    url = "http://www.youtube.com/get_video_info?&video_id=%s&el=$el&ps=default&eurl=%s&hl=en_US&t=%s" % (id, quote(eurl), quote(t))
    data = read_url(url)
    info = {}
    for part in data.split('&'):
        key, value = part.split('=')
        info[key] = unquote_plus(value).replace('+', ' ')
    return info

def find(query, max_results=10, offset=1, orderBy='relevance'):
    query = quote(query)
    url = "http://gdata.youtube.com/feeds/api/videos?vq=%s&orderby=%s&start-index=%s&max-results=%s" % (query, orderBy, offset, max_results)
    data = read_url(url)
    fd = feedparser.parse(data)
    videos = []
    for item in fd.entries:
        id = item['id'].split('/')[-1]
        title = item['title']
        description = item['description']
        videos.append((title, id, description))
        if len(videos) >= max_results:
            return videos
    return videos

def info(id, timeout=cache_timeout):
    info = {}
    if id.startswith('http'):
        id = get_id(id)
        if not id:
            return info
    url = "http://gdata.youtube.com/feeds/api/videos/%s?v=2" % id
    data = read_url(url, timeout=timeout)
    xml = parseString(data)
    info['id'] = id
    info['url'] = get_url(id)
    info['title'] = xml.getElementsByTagName('title')[0].firstChild.data
    info['description'] = xml.getElementsByTagName('media:description')[0].firstChild.data
    info['date'] = xml.getElementsByTagName('published')[0].firstChild.data.split('T')[0]
    info['author'] = "http://www.youtube.com/user/%s"%xml.getElementsByTagName('name')[0].firstChild.data

    info['categories'] = []
    for cat in xml.getElementsByTagName('media:category'):
        info['categories'].append(cat.firstChild.data)

    k = xml.getElementsByTagName('media:keywords')[0].firstChild
    if k:
        info['keywords'] = k.data.split(', ')
    data = read_url(info['url'], timeout=timeout)
    match = re.compile('<h4>License:</h4>(.*?)</p>', re.DOTALL).findall(data)
    if match:
        info['license'] = match[0].strip()
        info['license'] = re.sub('<.+?>', '', info['license']).strip()

    url = "http://www.youtube.com/api/timedtext?hl=en&type=list&tlangs=1&v=%s&asrs=1" % id
    data = read_url(url, timeout=timeout)
    xml = parseString(data)
    languages = [t.getAttribute('lang_code') for t in xml.getElementsByTagName('track')]
    if languages:
        info['subtitles'] = {}
        for language in languages:
            url = "http://www.youtube.com/api/timedtext?hl=en&v=%s&type=track&lang=%s&name&kind"%(id, language)
            data = read_url(url, timeout=timeout)
            xml = parseString(data)
            subs = []
            for t in xml.getElementsByTagName('text'):
                start = float(t.getAttribute('start'))
                duration = t.getAttribute('dur')
                if not duration:
                    duration = '2'
                end = start + float(duration)
                if t.firstChild:
                    text = t.firstChild.data
                    subs.append({
                        'in': start,
                        'out': end,
                        'value': ox.decode_html(text),
                    })
            info['subtitles'][language] = subs
    return info

def videos(id, format=''):
    stream_type = {
        'flv': 'video/x-flv',
        'webm': 'video/webm',
        'mp4': 'video/mp4'
    }.get(format)
    info = get_video_info(id)
    stream_map = info['url_encoded_fmt_stream_map']
    streams = {}
    for x in stream_map.split(','):
        stream = {}
        #for s in x.split('\\u0026'):
        for s in x.split('&'):
            key, value = s.split('=')
            value = unquote_plus(value)
            stream[key] = value
        if 'url' in stream and 'sig' in stream:
            stream['url'] = '%s&signature=%s' % (stream['url'], stream['sig'])
        if not stream_type or stream['type'].startswith(stream_type):
            streams[stream['itag']] = stream
    return streams

def playlist(url):
    data = read_url(url)
    items = []
    for i in list(set(re.compile('<a href="(/watch\?v=.*?)" title="(.*?)" ').findall(data))):
        items.append({
            'title': i[1],
            'url': 'http://www.youtube.com' + i[0].split('&amp;')[0]
        })
    return items

def download_webm(id, filename):
    stream_type = 'video/webm'
    url = "http://www.youtube.com/watch?v=%s" % id
    cj = cookielib.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [
        ('User-Agent',
         'Mozilla/5.0 (X11; Linux i686; rv:2.0) Gecko/20100101 Firefox/4.0'),
        ('Accept-Language', 'en-us, en;q=0.50')
    ]
    u = opener.open(url)
    data = u.read()
    u.close()
    match = re.compile('"url_encoded_fmt_stream_map": "(.*?)"').findall(data)
    streams = {}
    for x in match[0].split(','):
        stream = {}
        for s in x.split('\\u0026'):
            key, value = s.split('=')
            value = unquote_plus(value)
            stream[key] = value
        if stream['type'].startswith(stream_type):
            streams[stream['itag']] = stream
    if streams:
        s = max(streams.keys())
        url = streams[s]['url']
        if 'sig' in streams[s]:
            url += 'signature=' + streams[s]['sig']
    else:
        return None

    #download video and save to file.
    u = opener.open(url)
    f = open(filename, 'w')
    data = True
    while data:
        data = u.read(4096)
        f.write(data)
    f.close()
    u.close()
    return filename

def get_config(id):
    if id.startswith('http'):
        url = id
    else:
        url = get_url(id)
    data = read_url(url)
    match = re.compile('ytplayer.config = (.*?);<').findall(data)
    if match:
        config = json.load(match[0])
    return config
