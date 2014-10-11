# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
from __future__ import print_function
from datetime import datetime
import re
import time

import ox.cache
from ox.html import decode_html, strip_tags
import ox.net


def get_news(year, month, day):
    sections = [
        'politik', 'wirtschaft', 'panorama', 'sport', 'kultur', 'netzwelt',
        'wissenschaft', 'unispiegel', 'schulspiegel', 'reise', 'auto'
    ]
    dt = datetime(year, month, day)
    day = int(dt.strftime('%j'))
    date = dt.strftime('%d.%m.%Y')
    news = []
    for section in sections:
        url = 'http://www.spiegel.de/%s/0,1518,archiv-%d-%03d,00.html' % (section, year, day)
        if date == time.strftime('%d.%m.%Y', time.localtime()):
            html = ox.net.read_url(url)
        else:
            html = ox.cache.read_url(url)
        for item in re.compile('<div class="spTeaserCenterpage(.*?)</p>', re.DOTALL).findall(html):
            dateString = strip_tags(re.compile('<div class="spDateTime">(.*?)</div>', re.DOTALL).findall(item)[0]).strip()
            try:
                description = format_string(re.compile('<p>(.*?)<', re.DOTALL).findall(item)[0])
            except:
                description = ''
            try:
                imageUrl = re.compile('<img src="(.*?)"').findall(item)[0]
            except:
                imageUrl = ''
            try:
                title = format_string(re.compile('alt=[\'|"](.*?)[\'|"] title=', re.DOTALL).findall(item)[0]).replace(' : ', ': ').replace('::', ':')
            except:
                title = ''
            if dateString[:10] == date and description and imageUrl and title.find(': ') != -1:
                new = {}
                if len(dateString) == 10:
                    new['date'] = '%s-%s-%s 00:00' % (dateString[6:10], dateString[3:5], dateString[:2])
                else:
                    new['date'] = '%s-%s-%s %s:%s' % (dateString[6:10], dateString[3:5], dateString[:2], dateString[12:14], dateString[15:17])
                # fix decode_html
                # new['description'] = format_string(decode_html(description))
                new['description'] = format_string(description)
                new['imageUrl'] = imageUrl
                new['section'] = format_section(section)
                new['title'] = format_string(title)
                new['title1'] = new['title'].replace('\xdf', '\xdf\xdf')[:len(format_string(re.compile('<h4>(.*?)</h4>', re.DOTALL).findall(item)[0]))].replace('\xdf\xdf', '\xdf')
                if new['title1'][-1:] == ':':
                    new['title1'] = new['title1'][0:-1]
                new['title2'] = new['title'][len(new['title1']) + 2:]
                new['url'] = re.compile('<a href="(.*?)"').findall(item)[0]
                if new['url'][:1] == '/':
                    new['url'] = 'http://www.spiegel.de' + new['url']
                news.append(new)
                # print('%s, %s' % (new['section'], dateString))
            '''
            elif dateString[:10] == date and not description:
                print(dateString + ' - no description')
            elif dateString[:10] == date and not imageUrl:
                print(dateString + ' - no image')
            '''
    return news

def split_title(title):
    title1 = re.compile('(.*?): ').findall(title)[0]
    title2 = re.compile(': (.*?)$').findall(title)[0]
    return [title1, title2]

def format_string(string):
    string = string.replace('<span class="spOptiBreak"> </span>', '')
    string = string.replace('\n', ' ').replace('  ', ' ').strip()
    string = string.replace('&amp;', '&').replace('&apos;', '\'').replace('&quot;', '"')
    return string

def format_section(string):
    return string[:1].upper() + string[1:].replace('spiegel', 'SPIEGEL')

def format_subsection(string):
    # SPIEGEL, SPIEGEL special
    subsection = {
        'abi': 'Abi - und dann?',
        'formel1': 'Formel 1',
        'jobundberuf': 'Job & Beruf',
        'leben': 'Leben U21',
        'mensch': 'Mensch & Technik',
        'sonst': '',
        'staedte': u'St\xc3dte',
        'ussports': 'US-Sports',
        'wunderbar': 'wunderBAR'
    }
    if subsection.has_key(string):
        return subsection[string].replace(u'\xc3', 'ae')
    return string[:1].upper() + string[1:]
        
def get_issue(year, week):
    coverUrl = 'http://www.spiegel.de/static/epaper/SP/%d/%d/ROSPANZ%d%03d0001-312.jpg' % (year, week, year, week)
    if not ox.net.exists(coverUrl):
        return None
    url = 'http://service.spiegel.de/digas/servlet/epaper?Q=SP&JG=%d&AG=%d&SE=1&AN=INHALT' % (year, week)
    contents = []
    data = ox.cache.read_url(url)
    items = re.compile('<a.?href="http://service.spiegel.de/digas/servlet/epaper\?Q=SP&JG=".?>(.*?)</a>').findall(data)
    for item in items:
        item = item[1]
        page = int(re.compile('&amp;SE=(.*?)"').findall(item)[0])
        title = strip_tags(item).strip()
        contents.append({'title': title, 'page': page})
    pageUrl = {}
    pages = page + 2
    for page in range(1, pages + 10):
        url = 'http://www.spiegel.de/static/epaper/SP/%d/%d/ROSPANZ%d%03d%04d-205.jpg' % (year, week, year, week, page)
        if ox.cache.exists(url):
            pageUrl[page] = url
        else:
            pageUrl[page] = ''
    return {'pages': pages, 'contents': contents, 'coverUrl': coverUrl, 'pageUrl': pageUrl}


def archive_issues():
    '''
    this is just an example of an archiving application
    '''
    p = {}
    import os
    from ox.utils import json
    import time
    archivePath = '/Volumes/Rolux Home/Desktop/Data/spiegel.de/Der Spiegel'
    localtime = time.localtime()
    year = int(time.strftime('%Y', localtime))
    week = int(time.strftime('%W', localtime))
    for y in range(year, 1993, -1):
        if y == year:
            wMax = week + 1
        else:
            wMax = 53
        for w in range(wMax, 0, -1):
            print('get_issue(%d, %d)' % (y, w))
            issue = get_issue(y, w)
            if issue:
                dirname = '%s/%d/%02d' % (archivePath, y, w)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                filename = '%s/Der Spiegel %d %02d.json' % (dirname, y, w)
                if not os.path.exists(filename):
                    data = json.dumps(issue, ensure_ascii = False)
                    f = open(filename, 'w')
                    f.write(data)
                    f.close()
                filename = '%s/Der Spiegel %d %02d.txt' % (dirname, y, w)
                if not os.path.exists(filename):
                    data = []
                    for item in issue['contents']:
                        data.append('%3d %s' % (item['page'], item['title']))
                    data = '\n'.join(data)
                    f = open(filename, 'w')
                    f.write(data)
                    f.close()
                filename = '%s/Der Spiegel %d %02d.jpg' % (dirname, y, w)
                if not os.path.exists(filename):
                    data = ox.cache.read_url(issue['coverUrl'])
                    f = open(filename, 'w')
                    f.write(data)
                    f.close()
                for page in issue['pageUrl']:
                    url = issue['pageUrl'][page]
                    if url:
                        filename = '%s/Der Spiegel %d %02d %03d.jpg' % (dirname, y, w, page)
                        if not os.path.exists(filename):
                            data = ox.cache.read_url(url)
                            f = open(filename, 'w')
                            f.write(data)
                            f.close()
                if not p:
                    p = {'num': 1, 'sum': issue['pages'], 'min': issue['pages'], 'max': issue['pages']}
                else:
                    p['num'] += 1
                    p['sum'] += issue['pages']
                    if issue['pages'] < p['min']:
                        p['min'] = issue['pages']
                    if issue['pages'] > p['max']:
                        p['max'] = issue['pages']
                print(p['min'], p['sum'] / p['num'], p['max'])
            

def archive_news():
    '''
    this is just an example of an archiving application
    '''
    import os
    from ox.utils import json
    import time

    count = {}
    colon = []

    archivePath = '/Volumes/Rolux Home/Desktop/Data/spiegel.de/Spiegel Online'
    days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    localtime = time.localtime()
    year = int(time.strftime('%Y', localtime))
    month = int(time.strftime('%m', localtime))
    day = int(time.strftime('%d', localtime)) - 1
    for y in range(year, 1999, -1):
        if y == year:
            mMax = month
        else:
            mMax = 12
        for m in range(mMax, 0, -1):
            if y == year and m == month:
                dMax = day
            elif m == 2 and y % 4 == 0 and y % 400 != 0:
                dMax = days[m] + 1
            else:
                dMax = days[m]
            for d in range(dMax, 0, -1):
                print('getNews(%d, %d, %d)' % (y, m, d))
                news = getNews(y, m ,d)
                for new in news:
                    dirname = archivePath + '/' + new['date'][0:4] + '/' + new['date'][5:7] + new['date'][8:10] + '/' + new['date'][11:13] + new['date'][14:16]
                    if not os.path.exists(dirname):
                        os.makedirs(dirname)
                    if new['url'][-5:] == '.html':
                        filename = dirname + '/' + new['url'].split('/')[-1][:-5] + '.json'
                    else:
                        filename = dirname + '/' + new['url'] + '.json'
                    if not os.path.exists(filename) or True:
                        data = json.dumps(new, ensure_ascii = False)
                        f = open(filename, 'w')
                        f.write(data)
                        f.close()
                    filename = filename[:-5] + '.txt'
                    if not os.path.exists(filename) or True:
                        data = split_title(new['title'])
                        data.append(new['description'])
                        data = '\n'.join(data)
                        f = open(filename, 'w')
                        f.write(data)
                        f.close()
                    filename = dirname + '/' + new['imageUrl'].split('/')[-1]
                    if not os.path.exists(filename):
                        data = ox.cache.read_url(new['imageUrl'])
                        f = open(filename, 'w')
                        f.write(data)
                        f.close()

                    strings = new['url'].split('/')
                    string = strings[3]
                    if len(strings) == 6:
                        string += '/' + strings[4]
                    if not count.has_key(string):
                        count[string] = {'count': 1, 'string': '%s %s http://www.spiegel.de/%s/0,1518,archiv-%d-%03d,00.html' % (new['date'], new['date'], new['section'].lower(), y, int(datetime(y, m, d).strftime('%j')))}
                    else:
                        count[string] = {'count': count[string]['count'] + 1, 'string': '%s %s' % (new['date'], count[string]['string'][17:])}
                    strings = split_title(new['title'])
                    if strings[0] != new['title1'] or strings[1] != new['title2']:
                        colon.append('%s %s %s: %s' % (new['date'], new['title'], new['title1'], new['title2']))
            for key in sorted(count):
                print('%6d %-24s %s' % (count[key]['count'], key, count[key]['string']))
            for value in colon:
                print(value)

if __name__ == '__main__':
    # spiegel = Spiegel(2008, 8)
    # print(spiegel.getContents())
    # news = News(2001, 9, 10)
    # output(news.getNews())
    '''
    x = []
    for d in range(10, 30):
        print('2/%d' % d)
        news = getNews(2008, 2, d)
        for new in news:
            strings = new['url'].split('/')
            string = format_section(strings[3])
            if len(strings) == 6:
                string += '/' + format_subsection(strings[4])
            if not string in x:
                x.append(string)
        print(x)
    '''
    # archive_issues()
    archive_news()
