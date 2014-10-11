# vi:si:et:sw=4:sts=4:ts=4
# encoding: utf-8
from __future__ import print_function
import re
from six.moves.urllib.parse import urlencode

from ox.cache import read_url
from ox.html import decode_html, strip_tags
from ox.text import find_re
from ox.text import find_string


# to sniff itunes traffic, use something like
# sudo tcpdump -i en1 -Avs 8192 host appleglobal.112.2o7.net

# http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZSearch.woa/wa/advancedSearch?media=music&songTerm=&genreIndex=1&flavor=0&mediaType=2&composerTerm=&allArtistNames=Arcadia&ringtone=0&searchButton=submit
# http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZSearch.woa/wa/advancedSearch?media=movie&movieTerm=The%20Matrix&descriptionTerm=&ratingIndex=1&mediaType=3&directorProducerName=Andy%20Wachowski&flavor=0&releaseYearTerm=1999&closedCaption=0&actorTerm=&searchButton=submit

ITUNES_HEADERS = {
    'X-Apple-Tz': '0',
    'X-Apple-Storefront': '143441-1',
    'User-Agent': 'iTunes/7.6.2 (Macintosh; U; Intel Mac OS X 10.5.2)',
    'Accept-Language': 'en-us, en;q=0.50',
    'Accept-Encoding': 'gzip',
    'Connection': 'close',
}

def compose_url(request, parameters):
    if request == 'advancedSearch':
        url = 'http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZSearch.woa/wa/advancedSearch?'
        if parameters['media'] == 'music':
            url += urlencode({
              'albumTerm': parameters['title'],
              'allArtistNames': parameters['artist'],
              'composerTerm': '',
              'flavor': 0,
              'genreIndex': 1,
              'media': 'music',
              'mediaType': 2,
              'ringtone': 0,
              'searchButton': 'submit',
              'songTerm': ''
            })
        elif parameters['media'] == 'movie':
            url += urlencode({
              'actorTerm': '',
              'closedCaption': 0,
              'descriptionTerm': '',
              'directorProducerName': parameters['director'],
              'flavor': 0,
              'media': 'movie',
              'mediaType': 3,
              'movieTerm': parameters['title'],
              'ratingIndex': 1,
              'releaseYearTerm': '',
              'searchButton': 'submit'
            })
    elif request == 'viewAlbum':
        url = 'http://phobos.apple.com/WebObjects/MZStore.woa/wa/viewAlbum?id=%s' % parameters['id']
    elif request == 'viewMovie':
        url = 'http://phobos.apple.com/WebObjects/MZStore.woa/wa/viewMovie?id=%s&prvw=1' % parameters['id']
    return url

def parse_xml_dict(xml):
    values = {}
    strings = xml.split('<key>')
    for string in strings:
        if string.find('</key>') != -1:
            key = find_re(string, '(.*?)</key>')
            type = find_re(string, '</key><(.*?)>')
            if type == 'true/':
                value = True
            else:
                value = find_re(string, '<%s>(.*?)</%s>' % (type, type))
                if type == 'integer':
                  value = int(value)
                elif type == 'string':
                  value = decode_html(value)
            values[key] = value
    return values

def parse_cast(xml, title):
    list = []
    try:
        strings = find_re(xml, '<SetFontStyle normalStyle="textColor">%s(.*?)</VBoxView>' % title[:-1].upper()).split('</GotoURL>')
        strings.pop()
        for string in strings:
            list.append(find_re(string, '<SetFontStyle normalStyle="textColor">(.*?)</SetFontStyle>'))
        return list
    except:
        return list

def parse_movies(xml, title):
    list = []
    try:
        strings = find_re(xml, '<SetFontStyle normalStyle="outlineTitleFontStyle"><b>%s(.*?)</Test>' % title[:-1].upper()).split('</GotoURL>')
        strings.pop()
        for string in strings:
            list.append({
              'id': find_re(string, 'viewMovie\?id=(.*?)&'),
              'title': find_re(string, '<SetFontStyle normalStyle="outlineTextFontStyle"><b>(.*?)</b></SetFontStyle>')
            })
        return list
    except:
        return list

class ItunesAlbum:
    def __init__(self, id = '', title = '', artist = ''):
        self.id = id
        self.title = title
        self.artist = artist
        if not id:
            self.id = self.get_id()

    def get_id(self):
        url = compose_url('advancedSearch', {'media': 'music', 'title': self.title, 'artist': self.artist})
        xml = read_url(url, headers = ITUNES_HEADERS)
        id = find_re(xml, 'viewAlbum\?id=(.*?)&')
        return id

    def get_data(self):
        data = {'id': self.id}
        url = compose_url('viewAlbum', {'id': self.id})
        xml = read_url(url, None, ITUNES_HEADERS)
        data['albumName'] = find_re(xml, '<B>(.*?)</B>')
        data['artistName'] = find_re(xml, '<b>(.*?)</b>')
        data['coverUrl'] = find_re(xml, 'reflection="." url="(.*?)"')
        data['genre'] = find_re(xml, 'Genre:(.*?)<')
        data['releaseDate'] = find_re(xml, 'Released(.*?)<')
        data['review'] = strip_tags(find_re(xml, 'REVIEW</b>.*?<SetFontStyle normalStyle="textColor">(.*?)</SetFontStyle>'))
        data['tracks'] = []
        strings = find_re(xml, '<key>items</key>.*?<dict>(.*?)$').split('<dict>')
        for string in strings:
          data['tracks'].append(parse_xml_dict(string))
        data['type'] = find_re(xml, '<key>listType</key><string>(.*?)<')
        return data

class ItunesMovie:
    def __init__(self, id = '', title = '', director = ''):
        self.id = id
        self.title = title
        self.director = director
        if not id:
            self.id = self.get_id()

    def get_id(self):
        url = compose_url('advancedSearch', {'media': 'movie', 'title': self.title, 'director': self.director})
        xml = read_url(url, headers = ITUNES_HEADERS)
        id = find_re(xml, 'viewMovie\?id=(.*?)&')
        return id

    def get_data(self):
        data = {'id': self.id}
        url = compose_url('viewMovie', {'id': self.id})
        xml = read_url(url, None, ITUNES_HEADERS)
        f = open('/Users/rolux/Desktop/iTunesData.xml', 'w')
        f.write(xml)
        f.close()
        data['actors'] = parse_cast(xml, 'actors')
        string = find_re(xml, 'Average Rating:(.*?)</HBoxView>')
        data['averageRating'] = string.count('rating_star_000033.png') + string.count('&#189;') * 0.5
        data['directors'] = parse_cast(xml, 'directors')
        data['format'] = find_re(xml, 'Format:(.*?)<')
        data['genre'] = decode_html(find_re(xml, 'Genre:(.*?)<'))
        data['plotSummary'] = decode_html(find_re(xml, 'PLOT SUMMARY</b>.*?<SetFontStyle normalStyle="textColor">(.*?)</SetFontStyle>'))
        data['posterUrl'] = find_re(xml, 'reflection="." url="(.*?)"')
        data['producers'] = parse_cast(xml, 'producers')
        data['rated'] = find_re(xml, 'Rated(.*?)<')
        data['relatedMovies'] = parse_movies(xml, 'related movies')
        data['releaseDate'] = find_re(xml, 'Released(.*?)<')
        data['runTime'] = find_re(xml, 'Run Time:(.*?)<')
        data['screenwriters'] = parse_cast(xml, 'screenwriters')
        data['soundtrackId'] = find_re(xml, 'viewAlbum\?id=(.*?)&')
        data['trailerUrl'] = find_re(xml, 'autoplay="." url="(.*?)"')
        return data

if __name__ == '__main__':
    from ox.utils import json
    data = ItunesAlbum(title = 'So Red the Rose', artist = 'Arcadia').get_data()
    print(json.dumps(data, sort_keys = True, indent = 4))
    data = ItunesMovie(title = 'The Matrix', director = 'Wachowski').get_data()
    print(json.dumps(data, sort_keys = True, indent = 4))
    for v in data['relatedMovies']:
        data = ItunesMovie(id = v['id']).get_data()
        print(json.dumps(data, sort_keys = True, indent = 4))
    data = ItunesMovie(id='272960052').get_data()
    print(json.dumps(data, sort_keys = True, indent = 4))

