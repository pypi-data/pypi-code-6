# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import print_function

import re
import time
import unicodedata

from six.moves.urllib.parse import urlencode
from six import string_types

from .. import find_re, strip_tags, decode_html
from .. import cache


from . siteparser import SiteParser
from . import duckduckgo
from ..utils import datetime
from ..geo import normalize_country_name

def read_url(url, data=None, headers=cache.DEFAULT_HEADERS, timeout=cache.cache_timeout, valid=None, unicode=False):
    headers = headers.copy()
    return cache.read_url(url, data, headers, timeout, unicode=unicode)

def get_url(id):
    return "http://www.imdb.com/title/tt%s/" % id

class Imdb(SiteParser):
    '''
    >>> Imdb('0068646')['title']
    u'The Godfather'

    >>> Imdb('0133093')['title']
    u'The Matrix'
    '''
    regex =  {
        'alternativeTitles': {
            'page': 'releaseinfo',
            're': [
                'name="akas".*?<table.*?>(.*?)</table>',
                "td>(.*?)</td>.*?<td>(.*?)</td>"
            ],
            'type': 'list'
        
        },
        'aspectratio': {
            'page': 'combined',
            're': 'Aspect Ratio:</h5><div class="info-content">([\d\.]+)',
            'type': 'float',
        },
        'budget': {
            'page': 'business',
            're': [
                '<h5>Budget</h5>\s*?\$(.*?)<br',
                lambda data: find_re(decode_html(data).replace(',', ''), '\d+')
            ],
            'type': 'int'
        },
        'cast': {
            'page': 'combined',
            're': [
                '<td class="nm">.*?>(.*?)</a>.*?<td class="char">(.*?)</td>',
                lambda ll: [strip_tags(l) for l in ll]
             ],
            'type': 'list'
        },
        'cinematographer': {
            'page': 'combined',
            're': [
                lambda data: data.split('Series Crew')[0],
                'Cinematography by</a>(.*?)</table>',
                '<a href="/name/.*?/">(.*?)</a>'
            ],
            'type': 'list'
        },
        'connections': {
            'page': 'trivia?tab=mc',
            're': '<h4 class="li_group">(.*?)</h4>(.*?)(<\/div>\n  <a|<script)',
            'type': 'list'
        },
        'country': {
            'page': 'combined',
            're': [
                '<div class="info"><h5>Country:</h5>.*?<div class="info">',
                #'<a href="/country/.*?">(.*?)</a>', #links changed to work with existing caches, just take all links
                '<a.*?>(.*?)</a>',
            ],
            'type': 'list'
        },
        'creator': {
            'page': 'combined',
            're': [
                '<h5>Creator.?:</h5>.*?<div class="info-content">(.*?)</div>',
                '<a href="/name/.*?>(.*?)</a>'
            ],
            'type': 'list'
        },
        'director': {
            'page': 'combined',
            're': [
                lambda data: data.split('<b>Series Crew</b>')[0],
                'Directed by</a>(.*?)</table>',
                '<a href="/name/.*?>(.*?)</a>'
            ],
            'type': 'list'
        },
        '_director': {
            'page': 'combined',
            're': [
                '<h5>Director:</h5>.*?<div class="info-content">(.*?)</div>',
                '<a href="/name/.*?>(.*?)</a>'
            ],
            'type': 'list'
        },
        'editor': {
            'page': 'combined',
            're': [
                lambda data: data.split('Series Crew')[0],
                'Film Editing by</a>(.*?)</table>',
                '<a href="/name/.*?>(.*?)</a>'
            ],
            'type': 'list'
        },
        'composer': {
            'page': 'combined',
            're': [
                lambda data: data.split('Series Crew')[0],
                'Original Music by</a>(.*?)</table>',
                '<a href="/name/.*?>(.*?)</a>'
            ],
            'type': 'list'
        },
        'episodeTitle': {
            'page': 'combined',
            're': '<div id="tn15title">.*?<em>(.*?)</em>',
            'type': 'string'
        },
        'filmingLocations': {
            'page': 'locations',
            're': [
                '<a href="/search/title\?locations=.*?".*?>(.*?)</a>',
                lambda data: data.strip(),
            ],
            'type': 'list'
        },
        'genre': {
            'page': 'combined',
            're': [
                '<h5>Genre:</h5>(.*?)<hr',
                '<a href="/Sections/Genres/.*?/">(.*?)</a>'
            ],
            'type': 'list'
        },
        'gross': {
            'page': 'business',
            're': [
                '<h5>Gross</h5>\s*?\$(.*?)<br',
                lambda data: find_re(data.replace(',', ''), '\d+')
            ],
            'type': 'int'
        },
        'keyword': {
            'page': 'keywords',
            're': '<a href="/keyword/.*?>(.*?)</a>',
            'type': 'list'
        },
        'language': {
            'page': 'combined',
            're': [
                '<div class="info"><h5>Language:</h5>.*?<div class="info">',
                #'<a href="/language/.*?">(.*?)</a>', #links changed to work with existing caches, just take all links
                '<a.*?>(.*?)</a>',
            ],
            'type': 'list'
        },
        'summary': {
            'page': 'plotsummary',
            're': '<p class="plotSummary">(.*?)<\/p>',
            'type': 'string'
        },
        'posterId': {
            'page': 'combined',
            're': '/primary-photo/media/rm(.*?)/tt',
            'type': 'string'
        },
        'posterIds': {
            'page': 'posters',
            're': '/unknown-thumbnail/media/rm(.*?)/tt',
            'type': 'list'
        },
        'producer': {
            'page': 'combined',
            're': [
                lambda data: data.split('Series Crew')[0],
                'Produced by</a>(.*?)</table>',
                '<a href="/name/.*?/">(.*?)</a>'
            ],
            'type': 'list'
        },
        'productionCompany': {
            'page': 'combined',
            're': [
                'Production Companies</b><ul>(.*?)</ul>',
                '<a href="/company/.*?/">(.*?)</a>'
            ],
            'type': 'list'
        },
        'rating': {
            'page': 'combined',
            're': '<div class="starbar-meta">.*?<b>([\d,.]+?)/10</b>',
            'type': 'float'
        },
        'releasedate': {
            'page': 'releaseinfo',
            're': [
                '<td class="release_date">(.*?)</td>',
                strip_tags,
            ],
            'type': 'list'
        },
        'reviews': {
            'page': 'externalreviews',
            're': [
                '<ol>(.*?)</ol>',
                '<li><a href="(http.*?)".*?>(.*?)</a></li>'
            ],
            'type': 'list'
        },
        'runtime': {
            'page': 'combined',
            're': '<h5>Runtime:</h5><div class="info-content">.*?([0-9]+ sec|[0-9]+ min).*?</div>',
            'type': 'string'
        },
        'color': {
            'page': 'combined',
            're': [
                '<h5>Color:</h5><div class="info-content">(.*?)</div>',
                '<a.*?>(.*?)</a>'
            ],
            'type': 'list'
        },
        'sound': {
            'page': 'combined',
            're': [
                '<h5>Sound Mix:</h5><div class="info-content">(.*?)</div>',
                '<a.*?>(.*?)</a>'
            ],
            'type': 'list'
        },
        'season': {
            'page': 'combined',
            're': [
                '<h5>Original Air Date:</h5>.*?<div class="info-content">(.*?)</div>',
                '\(Season (\d+), Episode \d+\)',
             ],
            'type': 'int'
        },
        'episode': {
            'page': 'combined',
            're': [
                '<h5>Original Air Date:</h5>.*?<div class="info-content">(.*?)</div>',
                '\(Season \d+, Episode (\d+)\)',
             ],
            'type': 'int'
        },
        'series': {
            'page': 'combined',
            're': '<h5>TV Series:</h5>.*?<a href="/title/tt(\d{7})',
            'type': 'string'
        },
        'isSeries': {
            'page': 'combined',
            're': '<span class="tv-extra">(TV series|TV mini-series) ',
            'type': 'string'
        },
        'title': {
            'page': 'combined',
            're': '<h1>(.*?) <span>',
            'type': 'string'
        },
        'trivia': {
            'page': 'trivia',
            're': [
                '<div class="sodatext">(.*?)<(br|/div)',
                lambda data: data[0]
            ],
            'type': 'list',
        },
        'votes': {
            'page': 'combined',
            're': '<a href="ratings" class="tn15more">([\d,]*?) votes</a>',
            'type': 'string'
        },
        'writer': {
            'page': 'combined',
            're': [
                lambda data: data.split('Series Crew')[0],
                'Writing credits</a>(.*?)</table>',
                '<a href="/name/.*?/">(.*?)</a>'
            ],
            'type': 'list'
        },
        'year': {
            'page': 'combined',
            're': '="og:title" content="[^"]*?\((\d{4}).*?"',
            'type': 'int'
        }
    }

    def read_url(self, url, timeout):
        if not url in self._cache:
            self._cache[url] = read_url(url, timeout=timeout, unicode=True)
        return self._cache[url]

    def __init__(self, id, timeout=-1):
        #use akas.imdb.com to always get original title:
        #http://www.imdb.com/help/show_leaf?titlelanguagedisplay
        self.baseUrl = "http://akas.imdb.com/title/tt%s/" % id
        super(Imdb, self).__init__(timeout)
       
        url = self.baseUrl + 'combined' 
        page = self.read_url(url, timeout=-1)
        if '<title>IMDb: Page not found</title>' in page \
            or 'The requested URL was not found on our server.' in page:
            return
        if "<p>We're sorry, something went wrong.</p>" in page:
            time.sleep(1)
            super(Imdb, self).__init__(0)

        if 'alternativeTitles' in self:
            if len(self['alternativeTitles']) == 2 and \
               isinstance(self['alternativeTitles'][0], string_types):
               self['alternativeTitles'] = [self['alternativeTitles']]

        #normalize country names
        if 'country' in self:
            self['country'] = [normalize_country_name(c) or c for c in self['country']]

        if 'sound' in self:
            self['sound'] = list(set(self['sound']))

        types = {}
        stop_words = [ 
            'alternative spelling',
            'alternative title',
            'alternative transliteration',
            'closing credits title',
            'complete title',
            'IMAX version',
            'informal short title',
            'International (Spanish title)',
            'Japan (imdb display title)',
            'longer version',
            'new title',
            'original subtitled version',
            'pre-release title',
            'promotional abbreviation',
            'recut version',
            'reissue title',
            'restored version',
            'script title',
            'short title',
            '(subtitle)',
            'TV title',
            'working title',
            'World-wide (Spanish title)',
        ]
        #ignore english japanese titles
        #for movies that are not only from japan
        if ['Japan'] != self.get('country', []):
            stop_words += [
                'Japan (English title)'
            ]
        for t in self.get('alternativeTitles', []):
            for type in t[0].split('/'):
                type = type.strip()
                stop_word = False
                for key in stop_words:
                    if key in type:
                        stop_word = True
                        break
                if not stop_word:
                    if not type in types:
                        types[type] = []
                    types[type].append(t[1])
        titles = {}
        for type in types:
            for title in types[type]:
                if not title in titles:
                    titles[title] = []
                titles[title].append(type)
        def select_title(type):
            title = types[type][0]
            count = 0
            if len(types[type]) > 1:
                for t in types[type]:
                    if len(titles[t]) > count:
                        count = len(titles[t])
                        title = t
            return title

        #FIXME: does work in python2.6, possible to import from __future__?
        #types = {type: select_title(type) for type in types}
        _types = {}
        for type in types:
            _types[type] = select_title(type)
        types = _types

        regexps = [
            "^.+ \(imdb display title\) \(English title\)$",
            "^USA \(imdb display title\)$",
            "^International \(English title\)$",
            "^International \(English title\)$",
            "^UK \(imdb display title\)$",
            "^International \(.+\) \(English title\)$",
            "^World-wide \(English title\)$",
        ]
        if 'Hong Kong' in self.get('country', []):
            regexps += [
                "Hong Kong \(English title\)"
            ]
        english_countries = (
            'USA', 'UK', 'United States', 'United Kingdom',
            'Australia', 'New Zealand'
        )
        if not filter(lambda c: c in english_countries, self.get('country', [])):
            regexps += [
                "^[^(]+ \(English title\)$",
                "^.+ \(.+\) \(English title\)$",
                "^USA$",
                "^UK$",
                "^USA \(.+\)$",
                "^UK \(.+\)$",
                "^Australia \(.+\)$",
                "World-wide \(English title\)",
                "\(literal English title\)",
                "^International \(.+ title\)$",
                "^International \(.+\) \(.+ title\)$",
            ]
        for regexp in regexps:
            for type in types:
                if re.compile(regexp).findall(type):
                    #print types[type], type
                    self['internationalTitle'] = types[type]
                    break
            if 'internationalTitle' in self:
                break

        def cleanup_title(title):
            if title.startswith('"') and title.endswith('"'):
                title = title[1:-1]
            if title.startswith("'") and title.endswith("'"):
                title = title[1:-1]
            title = re.sub('\(\#[.\d]+\)', '', title)
            return title.strip()

        for t in ('title', 'internationalTitle'):
            if t in self:
                self[t] = cleanup_title(self[t])

        if 'internationalTitle' in self and \
            self.get('title', '').lower() == self['internationalTitle'].lower():
            del self['internationalTitle']

        if 'alternativeTitles' in self:
            alt = {}
            for t in self['alternativeTitles']:
                title = cleanup_title(t[1])
                if title not in (self.get('title'), self.get('internationalTitle')):
                    if title not in alt:
                        alt[title] = []
                    for c in t[0].split('/'):
                        if not '(working title)' in c:
                            c = c.replace('International', '').replace('World-wide', '').split('(')[0].strip()
                            if c:
                                alt[title].append(c)
            self['alternativeTitles'] = []
            for t in sorted(alt, key=lambda a: sorted(alt[a])):
                if alt[t]:
                    countries = sorted([normalize_country_name(c) or c for c in alt[t]])
                    self['alternativeTitles'].append((t, countries))
            if not self['alternativeTitles']:
                del self['alternativeTitles']

        if 'internationalTitle' in self:
            self['originalTitle'] = self['title']
            self['title'] = self.pop('internationalTitle')

        if 'runtime' in self and self['runtime']:
            if 'min' in self['runtime']: base=60
            else: base=1
            self['runtime'] = int(find_re(self['runtime'], '([0-9]+)')) * base
        if 'runtime' in self and not self['runtime']:
            del self['runtime']
        if 'votes' in self: self['votes'] = self['votes'].replace(',', '')

        if 'cast' in self:
            if isinstance(self['cast'][0], string_types):
                self['cast'] = [self['cast']]
            self['actor'] = [c[0] for c in self['cast']]
            def cleanup_character(c):
                c = c.replace('(uncredited)', '').strip()
                return c
            self['cast'] = [{'actor': x[0], 'character': cleanup_character(x[1])}
                            for x in self['cast']]

        if 'connections' in self:
            cc={}
            if len(self['connections']) == 3 and isinstance(self['connections'][0], string_types):
                self['connections'] = [self['connections']]
            for rel, data, _ in self['connections']:
                if isinstance(rel, bytes):
                    rel = rel.decode('utf-8')
                #cc[rel] = re.compile('<a href="/title/tt(\d{7})/">(.*?)</a>').findall(data)
                def get_conn(c):
                    r = {
                        'id': c[0],
                        'title': cleanup_title(c[1]),
                    }
                    description = c[2].split('<br />')
                    if len(description) == 2 and description[-1].strip() != '-':
                        r['description'] = description[-1].strip()
                    return r
                cc[rel] = list(map(get_conn, re.compile('<a href="/title/tt(\d{7})/">(.*?)</a>(.*?)<\/div', re.DOTALL).findall(data)))


            self['connections'] = cc

        for key in ('country', 'genre'):
            if key in self:
                self[key] = list(filter(lambda x: x.lower() != 'home', self[key]))
        #0092999
        if '_director' in self:
            if 'series' in self or 'isSeries' in self:
                self['creator'] = self.pop('_director')
            else:
                del self['_director']
        if 'isSeries' in self:
            del self['isSeries']
            self['isSeries'] = True
        if 'episodeTitle' in self:
            self['episodeTitle'] = re.sub('Episode \#\d+\.\d+', '', self['episodeTitle'])

        if 'series' in self:
            series = Imdb(self['series'], timeout=timeout)
            self['seriesTitle'] = series['title']
            if 'episodeTitle' in self:
                self['seriesTitle'] = series['title']
                if 'season' in self and 'episode' in self:
                    self['title'] = "%s (S%02dE%02d) %s" % (
                        self['seriesTitle'], self['season'], self['episode'], self['episodeTitle'])
                else:
                    self['title'] = "%s (S01) %s" % (self['seriesTitle'], self['episodeTitle'])
                    self['season'] = 1
                self['title'] = self['title'].strip()
            if 'director' in self:
                self['episodeDirector'] = self['director']

            if not 'creator' in series and 'director' in series:
                series['creator'] = series['director']
                if len(series['creator']) > 10:
                    series['creator'] = series['director'][:1]

            for key in ['creator', 'country']:
                if key in series:
                    self[key] = series[key]

            if 'year' in series:
                self['seriesYear'] = series['year']
                if not 'year' in self:
                    self['year'] = series['year']

            if 'year' in self:
                self['episodeYear'] = self['year']
            if 'creator' in self:
                self['seriesDirector'] = self['creator']
            if 'originalTitle' in self:
                del self['originalTitle']
        else:
            for key in ('seriesTitle', 'episodeTitle', 'season', 'episode'):
                if key in self:
                    del self[key]
        if 'creator' in self:
            if 'director' in self:
                self['episodeDirector'] = self['director']
            self['director'] = self['creator']

        #make lists unique but keep order
        for key in ('director', 'language'):
            if key in self:
                self[key] = [x for i,x in enumerate(self[key])
                             if x not in self[key][i+1:]]

        for key in ('actor', 'writer', 'producer', 'editor', 'composer'):
            if key in self:
                if isinstance(self[key][0], list):
                    self[key] = [i[0] for i in self[key] if i]
                self[key] = sorted(list(set(self[key])), key=lambda a: self[key].index(a))


        if 'budget' in self and 'gross' in self:
            self['profit'] = self['gross'] - self['budget']

        if 'releasedate' in self:
            def parse_date(d):
                try:
                    d = datetime.strptime(d, '%d %B %Y')
                except:
                    try:
                        d = datetime.strptime(d, '%B %Y')
                    except:
                        return 'x'
                return '%d-%02d-%02d' % (d.year, d.month, d.day)
            self['releasedate'] = min([
                parse_date(d) for d in self['releasedate']
            ])
            if self['releasedate'] == 'x':
                del self['releasedate']
        if 'summary' in self:
            if isinstance(self['summary'], list):
                self['summary'] = self['summary'][0]
            self['summary'] = self['summary'].split('</p')[0].strip()

class ImdbCombined(Imdb):
    def __init__(self, id, timeout=-1):
        _regex = {}
        for key in self.regex:
            if self.regex[key]['page'] in ('combined', 'releaseinfo'):
                _regex[key] = self.regex[key]
        self.regex = _regex
        super(ImdbCombined, self).__init__(id, timeout)

def get_movie_by_title(title, timeout=-1):
    '''
    This only works for exact title matches from the data dump
    Usually in the format
        Title (Year)
        "Series Title" (Year) {(#Season.Episode)}
        "Series Title" (Year) {Episode Title (#Season.Episode)}

    If there is more than one film with that title for the year
        Title (Year/I)

    >>> get_movie_by_title(u'"Father Knows Best" (1954) {(#5.34)}')
    u'1602860'

    >>> get_movie_by_title(u'The Matrix (1999)')
    u'0133093'

    >>> get_movie_by_title(u'Little Egypt (1951)')
    u'0043748'

    >>> get_movie_by_title(u'Little Egypt (1897/I)')
    u'0214882'
    
    >>> get_movie_by_title(u'Little Egypt')
    None 

    >>> get_movie_by_title(u'"Dexter" (2006) {Father Knows Best (#1.9)}')
    u'0866567'
    '''
    params = {'s':'tt','q': title}
    if not isinstance(title, bytes):
        try:
            params['q'] = unicodedata.normalize('NFKC', params['q']).encode('latin-1')
        except:
            params['q'] = params['q'].encode('utf-8')
    params = urlencode(params)
    url = "http://akas.imdb.com/find?" + params
    data = read_url(url, timeout=timeout, unicode=True)
    #if search results in redirect, get id of current page
    r = '<meta property="og:url" content="http://www.imdb.com/title/tt(\d{7})/" />'
    results = re.compile(r).findall(data)    
    if results:
        return results[0]
    return None
 
def get_movie_id(title, director='', year='', timeout=-1):
    '''
    >>> get_movie_id('The Matrix')
    u'0133093'

    >>> get_movie_id('2 or 3 Things I Know About Her', 'Jean-Luc Godard')
    u'0060304'

    >>> get_movie_id('2 or 3 Things I Know About Her', 'Jean-Luc Godard', '1967')
    u'0060304'

    >>> get_movie_id(u"Histoire(s) du cinema: Le controle de l'univers", 'Jean-Luc Godard')
    u'0179214'

    >>> get_movie_id(u"Histoire(s) du cinéma: Le contrôle de l'univers", 'Jean-Luc Godard')
    u'0179214'
    '''
    imdbId = {
        (u'Le jour se l\xe8ve', u'Marcel Carn\xe9'): '0031514',
        (u'Wings', u'Larisa Shepitko'): '0061196',
        (u'The Ascent', u'Larisa Shepitko'): '0075404',
        (u'Fanny and Alexander', u'Ingmar Bergman'): '0083922',
        (u'Torment', u'Alf Sj\xf6berg'): '0036914',
        (u'Crisis', u'Ingmar Bergman'): '0038675',
        (u'To Joy', u'Ingmar Bergman'): '0043048',
        (u'Humain, trop humain', u'Louis Malle'): '0071635',
        (u'Place de la R\xe9publique', u'Louis Malle'): '0071999',
        (u'God\u2019s Country', u'Louis Malle'): '0091125',
        (u'Flunky, Work Hard', u'Mikio Naruse'): '0022036',
        (u'The Courtesans of Bombay', u'Richard Robbins') : '0163591',
        (u'Je tu il elle', u'Chantal Akerman') : '0071690',
        (u'Hotel Monterey', u'Chantal Akerman') : '0068725',
        (u'No Blood Relation', u'Mikio Naruse') : '023261',
        (u'Apart from You', u'Mikio Naruse') : '0024214',
        (u'Every-Night Dreams', u'Mikio Naruse') : '0024793',
        (u'Street Without End', u'Mikio Naruse') : '0025338',
        (u'Sisters of the Gion', u'Kenji Mizoguchi') : '0027672',
        (u'Osaka Elegy', u'Kenji Mizoguchi') : '0028021',
        (u'Blaise Pascal', u'Roberto Rossellini') : '0066839',
        (u'Japanese Girls at the Harbor', u'Hiroshi Shimizu') : '0160535',
        (u'The Private Life of Don Juan', u'Alexander Korda') : '0025681',
        (u'Last Holiday', u'Henry Cass') : '0042665',
        (u'A Colt Is My Passport', u'Takashi  Nomura') : '0330536',
        (u'Androcles and the Lion', u'Chester Erskine') : '0044355',
        (u'Major Barbara', u'Gabriel Pascal') : '0033868',
        (u'Come On Children', u'Allan King') : '0269104',

        (u'Jimi Plays Monterey & Shake! Otis at Monterey', u'D. A. Pennebaker and Chris Hegedus') : '',
        (u'Martha Graham: Dance on Film', u'Nathan Kroll') : '',
        (u'Carmen', u'Carlos Saura'): '0085297',
        (u'The Story of a Cheat', u'Sacha Guitry'): '0028201',
        (u'Weekend', 'Andrew Haigh'): '1714210',
    }.get((title, director), None)
    if imdbId:
        return imdbId
    params = {'s':'tt','q': title}
    if director:
        params['q'] = u'"%s" %s' % (title, director)
    if year:
        params['q'] = u'"%s (%s)" %s' % (title, year, director)
    google_query = "site:imdb.com %s" % params['q']
    if not isinstance(params['q'], bytes):
        try:
            params['q'] = unicodedata.normalize('NFKC', params['q']).encode('latin-1')
        except:
            params['q'] = params['q'].encode('utf-8')
    params = urlencode(params)
    url = "http://akas.imdb.com/find?" + params
    #print url

    data = read_url(url, timeout=timeout, unicode=True)
    #if search results in redirect, get id of current page
    r = '<meta property="og:url" content="http://www.imdb.com/title/tt(\d{7})/" />'
    results = re.compile(r).findall(data)    
    if results:
        return results[0]
    #otherwise get first result
    r = '<td valign="top">.*?<a href="/title/tt(\d{7})/"'
    results = re.compile(r).findall(data)
    if results:
        return results[0]

    #print (title, director), ": '',"
    #print google_query
    #results = google.find(google_query, timeout=timeout)
    results = duckduckgo.find(google_query, timeout=timeout)
    if results:
        for r in results[:2]:
            imdbId = find_re(r[1], 'title/tt(\d{7})')
            if imdbId:
                return imdbId
    #or nothing
    return ''

def get_movie_poster(imdbId):
    '''
    >>> get_movie_poster('0133093')
    'http://ia.media-imdb.com/images/M/MV5BMjEzNjg1NTg2NV5BMl5BanBnXkFtZTYwNjY3MzQ5._V1._SX338_SY475_.jpg'

    >>> get_movie_poster('0994352')
    'http://ia.media-imdb.com/images/M/MV5BMjA3NzMyMzU1MV5BMl5BanBnXkFtZTcwNjc1ODUwMg@@._V1._SX594_SY755_.jpg'
    '''
    info = ImdbCombined(imdbId)
    if 'posterId' in info:
        url = "http://www.imdb.com/media/rm%s/tt%s" % (info['posterId'], imdbId)
        data = read_url(url).decode('utf-8', 'ignore')
        poster = find_re(data, 'img.*?id="primary-img".*?src="(.*?)"')
        return poster
    elif 'series' in info:
        return get_movie_poster(info['series'])
    return ''

def get_episodes(imdbId, season=None):
    episodes = {}
    url = 'http://www.imdb.com/title/tt%s/episodes' % imdbId
    if season:
        url += '?season=%d' % season
        data = cache.read_url(url)
        for e in re.compile('<div data-const="tt(\d{7})".*?>.*?<div>S(\d+), Ep(\d+)<\/div>\n<\/div>', re.DOTALL).findall(data):
            episodes['S%02dE%02d' %(int(e[1]), int(e[2]))] = e[0]
    else:
        data = cache.read_url(url)
        match = re.compile('<strong>Season (\d+)</strong>').findall(data)
        if match:
            for season in range(1, int(match[0]) + 1):
               episodes.update(get_episodes(imdbId, season))
    return episodes

def max_votes():
    url = 'http://www.imdb.com/search/title?num_votes=500000,&sort=num_votes,desc'
    data = cache.read_url(url)
    votes = max([int(v.replace(',', ''))
        for v in re.compile('<td class="sort_col">([\d,]+)</td>').findall(data)])
    return votes

def guess(title, director='', timeout=-1):
    return get_movie_id(title, director, timeout=timeout)

if __name__ == "__main__":
    import json
    print(json.dumps(Imdb('0306414'), indent=2))
    #print json.dumps(Imdb('0133093'), indent=2)

