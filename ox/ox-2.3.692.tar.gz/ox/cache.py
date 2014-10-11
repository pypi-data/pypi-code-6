# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2011
from __future__ import with_statement, print_function

import gzip
import zlib
import hashlib
import os
from six import BytesIO
import time
from six.moves import urllib
from six import PY2
import sqlite3

from .utils import json
from .file import makedirs

from . import net
from .net import DEFAULT_HEADERS, detect_encoding

cache_timeout = 30*24*60*60 # default is 30 days

COMPRESS_TYPES = (
    'text/html',
    'text/plain',
    'text/xml',
    'application/json',
    'application/xhtml+xml',
    'application/x-javascript',
    'application/javascript',
    'application/ecmascript',
    'application/rss+xml'
)

def status(url, data=None, headers=DEFAULT_HEADERS, timeout=cache_timeout):
    '''
      >>> status('http://google.com')
      200
      >>> status('http://google.com/mysearch')
      404
    '''
    headers = get_headers(url, data, headers)
    return int(headers['status'])

def exists(url, data=None, headers=DEFAULT_HEADERS, timeout=cache_timeout):
    '''
      >>> exists('http://google.com')
      True
      >>> exists('http://google.com/mysearch')
      False
    '''
    s = status(url, data, headers, timeout)
    if s >= 200 and s < 400:
        return True
    return False

def get_headers(url, data=None, headers=DEFAULT_HEADERS, timeout=cache_timeout):
    url_headers = store.get(url, data, headers, timeout, "headers")
    if not url_headers:
        url_headers = net.get_headers(url, data, headers)
        store.set(url, data, -1, url_headers)
    return url_headers

def get_json(url, data=None, headers=DEFAULT_HEADERS, timeout=cache_timeout):
    return json.loads(read_url(url, data, headers, timeout).decode('utf-8'))

class InvalidResult(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, result, headers):
        self.result = result
        self.headers = headers

def _fix_unicode_url(url):
    if not isinstance(url, bytes):
        url = url.encode('utf-8')
    return url

def read_url(url, data=None, headers=DEFAULT_HEADERS, timeout=cache_timeout, valid=None, unicode=False):
    '''
        url     - url to load
        data    - possible post data
        headers - headers to send with request
        timeout - get from cache if cache not older than given seconds, -1 to get from cache
        valid   - function to check if result is ok, its passed result and headers
                  if this function fails, InvalidResult will be raised deal with it in your code 
    '''
    if net.DEBUG:
        print('ox.cache.read_url', url)
    #FIXME: send last-modified / etag from cache and only update if needed
    #url = _fix_unicode_url(url)
    result = store.get(url, data, headers, timeout)
    url_headers = {}
    if not result:
        try:
            url_headers, result = net.read_url(url, data, headers, return_headers=True)
        except urllib.error.HTTPError as e:
            e.headers['Status'] = "%s" % e.code
            for key in e.headers:
                url_headers[key.lower()] = e.headers[key]
            result = e.read()
            if url_headers.get('content-encoding', None) == 'gzip':
                result = gzip.GzipFile(fileobj=BytesIO(result)).read()
        if not valid or valid(result, url_headers):
            store.set(url, post_data=data, data=result, headers=url_headers)
        else:
            raise InvalidResult(result, url_headers)
    if unicode:
        ctype = url_headers.get('content-type', '').lower()
        if 'charset' in ctype:
            encoding = ctype.split('charset=')[-1]
        else:
            encoding = detect_encoding(result)
        if not encoding:
            encoding = 'latin-1'
        result = result.decode(encoding)
    return result

get_url=read_url

def save_url(url, filename, overwrite=False):
    if not os.path.exists(filename) or overwrite:
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        data = read_url(url)
        with open(filename, 'wb') as f:
            f.write(data)

def cache_path():
    return os.environ.get('oxCACHE', os.path.expanduser('~/.ox/cache'))

class Cache:
    def __init__(self):
        pass

    def get(self, url, data, headers=DEFAULT_HEADERS, timeout=-1, value="data"):
        '''
            if value == 'data' return data of url if its in the cache else None
            if value == 'headers' return headers for url
        '''
        pass

    def set(self, url, post_data, data, headers):
        pass

class SQLiteCache(Cache):
    def __init__(self):
        path = cache_path()
        if not os.path.exists(path):
            os.makedirs(path)
        self.db = os.path.join(path, "cache.sqlite")
        self.create()

    def connect(self):
        self.conn = sqlite3.connect(self.db, timeout=10)
        return self.conn

    def create(self):
        conn = self.connect()
        c = conn.cursor()
        # Create table and indexes 
        c.execute('''CREATE TABLE IF NOT EXISTS cache (url_hash varchar(42) unique, domain text, url text,
                          post_data text, headers text, created int, data blob, only_headers int)''')
        c.execute('''CREATE INDEX IF NOT EXISTS cache_domain ON cache (domain)''')
        c.execute('''CREATE INDEX IF NOT EXISTS cache_url ON cache (url)''')
        c.execute('''CREATE INDEX IF NOT EXISTS cache_url_hash ON cache (url_hash)''')

        c.execute('''CREATE TABLE IF NOT EXISTS setting (key varchar(1024) unique, value text)''')
        if int(self.get_setting(c, 'version', 0)) < 1:
            self.set_setting(c, 'version', 1)
            c.execute('''ALTER TABLE cache ADD compressed INT DEFAULT 0''')
            conn.commit()
    
    def get_setting(self, c, key, default=None):
        c.execute('SELECT value FROM setting WHERE key = ?', (key, ))
        for row in c:
            return row[0]
        return default

    def set_setting(self, c, key, value):
        c.execute(u'INSERT OR REPLACE INTO setting values (?, ?)', (key, str(value)))

    def get(self, url, data={}, headers=DEFAULT_HEADERS, timeout=-1, value="data"):
        r = None
        if timeout == 0:
            return r
        if data:
            url_hash = hashlib.sha1((url + '?' + data).encode('utf-8')).hexdigest()
        else:
            url_hash = hashlib.sha1(url.encode('utf-8')).hexdigest()

        conn = self.connect()
        c = conn.cursor()
        sql = 'SELECT %s, compressed FROM cache WHERE url_hash=?' % value
        if timeout > 0:
            now = time.mktime(time.localtime())
            t = (url_hash, now-timeout)
            sql += ' AND created > ?'
        else:
            t = (url_hash, )
        if value != "headers":
            sql += ' AND only_headers != 1 '
        c.execute(sql, t)
        for row in c:
            r = row[0]
            if value == 'headers':
                r = json.loads(r)
            elif value == 'data':
                if row[1] == 1:
                    r = zlib.decompress(r)
                elif PY2:
                    r = str(r)
            break

        c.close()
        conn.close()
        return r

    def set(self, url, post_data, data, headers):
        if post_data:
            url_hash = hashlib.sha1((url + '?' + post_data).encode('utf-8')).hexdigest()
        else:
            url_hash = hashlib.sha1(url.encode('utf-8')).hexdigest()

        domain = ".".join(urllib.parse.urlparse(url)[1].split('.')[-2:])

        conn = self.connect()
        c = conn.cursor()

        # Insert a row of data
        if not post_data: post_data=""
        only_headers = 0
        if data == -1:
            only_headers = 1
            data = ""
        created = time.mktime(time.localtime())
        content_type = headers.get('content-type', '').split(';')[0].strip()
        if content_type in COMPRESS_TYPES:
            compressed = 1
            data = zlib.compress(data)
        else:
            compressed = 0
        data = sqlite3.Binary(data)

        #fixme: this looks wrong
        try:
            _headers = json.dumps(headers)
        except:
            for h in headers:
                headers[h] = headers[h].decode(detect_encoding(headers[h]))
            _headers = json.dumps(headers)
        t = (url_hash, domain, url, post_data, _headers, created,
             data, only_headers, compressed)
        c.execute(u"""INSERT OR REPLACE INTO cache values (?, ?, ?, ?, ?, ?, ?, ?, ?)""", t)

        # Save (commit) the changes and clean up
        conn.commit()
        c.close()
        conn.close()

class FileCache(Cache):
    def __init__(self):
        f, self.root = cache_path().split(':')

    def files(self, domain, h):
        prefix = os.path.join(self.root, domain, h[:2], h[2:4], h[4:6], h[6:8])
        i = os.path.join(prefix, '%s.json'%h)
        f = os.path.join(prefix, '%s.dat'%h)
        return prefix, i, f
 
    def get(self, url, data={}, headers=DEFAULT_HEADERS, timeout=-1, value="data"):
        r = None
        if timeout == 0:
            return r

        if data:
            url_hash = hashlib.sha1((url + '?' + data).encode('utf-8')).hexdigest()
        else:
            url_hash = hashlib.sha1(url.encode('utf-8')).hexdigest()

        domain = ".".join(urllib.parse.urlparse(url)[1].split('.')[-2:])
        prefix, i, f = self.files(domain, url_hash)
        if os.path.exists(i):
            with open(i) as _i:
                try:
                    info = json.load(_i)
                except:
                    return r
            now = time.mktime(time.localtime())
            expired = now-timeout

            if value != 'headers' and info['only_headers']:
                return None
            if timeout < 0 or info['created'] > expired:
                if value == 'headers':
                    r = info['headers']
                else:
                    with open(f, 'rb') as data:
                        r = data.read()
                    if info['compressed']:
                        r = zlib.decompress(r)
        return r

    def set(self, url, post_data, data, headers):
        if post_data:
            url_hash = hashlib.sha1((url + '?' + post_data).encode('utf-8')).hexdigest()
        else:
            url_hash = hashlib.sha1(url.encode('utf-8')).hexdigest()

        domain = ".".join(urllib.parse.urlparse(url)[1].split('.')[-2:])
        prefix, i, f = self.files(domain, url_hash)
        makedirs(prefix)

        created = time.mktime(time.localtime())
        content_type = headers.get('content-type', '').split(';')[0].strip()

        info = {
            'compressed': content_type in COMPRESS_TYPES,
            'only_headers': data == -1,
            'created': created,
            'headers': headers,
            'url': url,
        }
        if post_data:
            info['post_data'] = post_data
        if not info['only_headers']:
            if info['compressed']:
                data = zlib.compress(data)
            elif not isinstance(data, str):
                data = data.encode('utf-8')
            with open(f, 'wb') as _f:
                _f.write(data)
        with open(i, 'wb') as _i:
            json.dump(info, _i)

if cache_path().startswith('fs:'):
    store = FileCache()
else:
    store = SQLiteCache()

