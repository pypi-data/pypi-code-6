from __future__ import print_function
import json
import re

from ox.cache import read_url

HEADERS = {
    'User-Agent': 'iTunes/10.4 (Macintosh; Intel Mac OS X 10.7) AppleWebKit/534.48.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us, en;q=0.50',
    'X-Apple-Store-Front': '143441-1,12',
    'X-Apple-Tz': '7200',
    'Accept-Encoding': 'gzip, deflate'
}
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7) '
USER_AGENT += 'AppleWebKit/534.48.3 (KHTML, like Gecko) Version/5.1 Safari/534.48.3'

def get_movie_data(title, director):
    if isinstance(title, unicode):
        title = title.encode('utf-8')
    if isinstance(director, unicode):
        director = director.encode('utf-8')
    data = {}
    # itunes section (preferred source for link)
    url = 'http://ax.search.itunes.apple.com/WebObjects/MZSearch.woa/wa/advancedSearch'
    url += '?media=movie&movieTerm=' + title
    url += '&actorNames=&directorProducerName=' + director
    url += '&releaseYearTerm=&descriptionTerm=&genreIndex=1&ratingIndex=1'
    HEADERS['Referer'] = url
    html = read_url(url, headers=HEADERS, unicode=True)
    regexp = '<a href="(http://itunes.apple.com/us/movie/.*?)" class="artwork-link"><div class="artwork">'
    regexp += '<img width=".*?" height=".*?" alt=".*?" class="artwork" src="(.*?)" /></div></a>'
    results = re.compile(regexp).findall(html)
    if results:
        data['link'] = results[0][0]
        data['poster'] = results[0][1].replace('140x140', '600x600')
        html = read_url(data['link'], headers=HEADERS, unicode=True)
        results = re.compile('video-preview-url="(.*?)"').findall(html)
        if results:
            data['trailer'] = results[0]
    # trailers section (preferred source for poster and trailer)
    host = 'http://trailers.apple.com'
    url = host + '/trailers/home/scripts/quickfind.php?callback=searchCallback&q=' + title
    js = json.loads(read_url(url, unicode=True)[16:-4])
    results = js['results']
    if results:
        url = host + results[0]['location']
        if not 'link' in data:
            data['link'] = url
        headers = {
            'User-Agent': USER_AGENT
        }
        html = read_url(url, headers=headers, unicode=True)
        results = re.compile('"(' + host + '.*?poster\.jpg)"').findall(html)
        if results:
            data['poster'] = results[0].replace('poster.jpg', 'poster-xlarge.jpg')
        html = read_url(url + 'includes/playlists/web.inc', headers=headers, unicode=True)
        results = re.compile('"(' + host + '\S+\.mov)"').findall(html)
        if results:
            data['trailer'] = results[-1]
    return data

if __name__ == '__main__':
    print(get_movie_data('Alphaville', 'Jean-Luc Godard'))
    print(get_movie_data('Sin City', 'Roberto Rodriguez'))
    print(get_movie_data('Breathless', 'Jean-Luc Godard'))
    print(get_movie_data('Capitalism: A Love Story', 'Michael Moore'))
    print(get_movie_data('Film Socialisme', 'Jean-Luc Godard'))
