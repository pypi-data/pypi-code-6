# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import re
import string
import subprocess
import ox
import os

def get_ids():
    result = []
    for i in string.ascii_uppercase:
        url = "http://www.filmsdivision.org/search.php?title=%s" % i
        data = ox.cache.read_url(url)
        links = re.compile('view_video.php\?movId=(.*?)[\'"]', re.DOTALL).findall(data)
        result += links
    return list(set(result))

def get_data(id):
    result = {}
    url = "http://www.filmsdivision.org/view_video.php?movId=%s" % id
    data = ox.cache.read_url(url)
    result['title'] = re.compile('<td.*?class="vdoheadtxt".*?>(.*?)</td>').findall(data)[0]
    result['year'] = re.compile('Release: (\d{4})').findall(data)[0]
    result['duration'] = int(re.compile('Duration: (\d+)mins').findall(data)[0]) * 60
    result['producer'] = re.compile('Producer: (.*?)\t').findall(data)[0].strip()
    if 'Director:' in data:
        result['director'] = re.compile('Director: (.*?)\t').findall(data)[0].strip()
    else:
        result['director'] = "Unknown Director"
    result['url'] = re.compile('value="(.*?.wmv)"').findall(data)[0]
    return result

def download_video(url, filename):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    p = subprocess.Popen(['gst-launch', 'mmssrc', 'location=%s'%url, '!', 'filesink', 'locaiton='%filename])
    p.wait()
    return p.returncode == 0
