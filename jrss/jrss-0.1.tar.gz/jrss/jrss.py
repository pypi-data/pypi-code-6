#coding: utf-8

from configobj import ConfigObj
from opster import command
import feedparser
import os
import requests
import time

HOME = os.getenv('USERPROFILE') or os.getenv('HOME')
CONF_PATH = os.path.join(HOME, '.jrssrc')

def write_template_config():
    conf = ConfigObj(
        CONF_PATH,
        create_empty=True,
        write_empty_values=True
    )

    conf['torrent_files_path'] = '/mnt/hdd0/torrent_files/'
    conf['shows'] = ['the.big.bang.theory', 'modern.family']
    conf['exclude'] = ['german', 'dubbed']
    conf['filter'] = ['720p']
    conf['rss_url'] = "http://example.com/rss?passkey=secret,key"

    conf.write()

def get_conf():
    if os.path.exists(CONF_PATH):
        return ConfigObj(CONF_PATH)
    else:
        write_template_config()
        print("Wrote example config to {0}".format(CONF_PATH))
        exit(0)

CONF = get_conf()

def download(item):
    # Remove items not in shows
    for show in CONF['shows']:
        show_low = show.lower()
        show_under = show_low.replace('.', '_')
        title = item['title'].lower()
        if show_low in title or show_under in title:
            break
    else:
        return
    
    # Remove items not in filter 
    for include in CONF['filter']:
        if not include.lower() in item['title'].lower():
            return

    # Remove items in exclude
    for exclude in CONF['exclude']:
        if exclude.lower() in item['title'].lower():
            return
    
    torrent_path = os.path.join(CONF['torrent_files_path'],
                                item['title'] + '.torrent')

    torrent_memory_path = os.path.join(CONF['torrent_files_path'],
                                '.' + item['title'] + '.torrent.mem')
    
    if os.path.exists(torrent_memory_path):
        return

    open(torrent_memory_path, 'w+')
    with open(torrent_path, 'w+') as fh:
        res = requests.get(item['link'])
        if not res.ok:
            return

        for block in res.iter_content(1024):
            if not block:
                break
            fh.write(block)

@command()
def main():
    for filename in os.listdir(CONF['torrent_files_path']):
        if filename[0] == "." and filename.endswith('.torrent.mem'):
            path = os.path.join(CONF['torrent_files_path'], filename)
            creation_time = os.path.getctime(path)
            yesterday = time.time()-60*60*24
            if creation_time < yesterday:
                os.unlink(path)
    f = feedparser.parse(CONF['rss_url'])
    for item in f['entries']:
        download(item)
