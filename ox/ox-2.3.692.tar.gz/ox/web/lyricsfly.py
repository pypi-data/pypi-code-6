# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import print_function

from ox.cache import read_url
from ox.html import decode_html
from ox.text import find_re


def get_lyrics(title, artist):
    html = read_url('http://lyricsfly.com/api/')
    key = find_re(html, '<font color=green><b>(.*?)</b></font>')
    url = 'http://lyricsfly.com/api/api.php?i=%s&a=%s&t=%s' % (key, artist, title)
    xml = read_url(url)
    lyrics = find_re(xml, '<tx>(.*?)\[br\] Lyrics [a-z]* by lyricsfly.com')
    lyrics = lyrics.replace('\n', '').replace('\r', '')
    lyrics = lyrics.replace('[br]', '\n').strip()
    lyrics.replace('\n\n\n', '\n\n')
    lyrics = decode_html(lyrics.replace('&amp;', '&'))
    return lyrics

if __name__ == '__main__':
    print(get_lyrics('Election Day', 'Arcadia'))
