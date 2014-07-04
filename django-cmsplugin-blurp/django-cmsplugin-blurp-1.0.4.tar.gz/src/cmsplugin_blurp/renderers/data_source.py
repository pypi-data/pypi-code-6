import logging
import hashlib
from xml.etree import ElementTree as ET
import time
import threading

import feedparser
import requests
from requests.exceptions import RequestException, HTTPError, Timeout

from django.core.cache import cache

from . import signature, template

log = logging.getLogger(__name__)


class Renderer(template.TemplateRenderer):
    '''Data source renderer the expected configuration looks like
       this:

           {
              'name': u'Datas from xyz',
              'class': 'cmsplugin_blurp.renderers.data_source.Renderer',
              'sources': [
                  {
                     'slug': 'slug', # mandatory
                     'url': 'https://...', # mandatory
                     'parser_type': 'raw', # optional, possible values are json, xml, css, csv or raw, default value is raw
                     'content_type': 'application/octet-stream', # optional, default value is compute from the parser_type
                     'auth_mech': None, # optional, possible values are hmac-sha1, hmac-sha256,oauth2', default is None
                     'signature_key': None, # mandatory if auth_mech is not None
                     'verify_certificate': False, # optional, default is False
                     'allow_redirects': True, # optional default is True
                     'timeout': 10, # optional default is 1, it cannot be less than 1
                     'refresh': 3600, # optional, default is taken from the renderer level
                     'limit': 0, # optional, default is taken from the renderer level
                  },
              ]
              'template_name': 'data_from_xyz.html'
              # default template if the template file cannot be found
              'template': '{{ slug|pprint }}'
              # time between refresh of the case
              # use 0 for no cache
              # cache is also update if updatecache key is in the query string
              # you can also override it in each source
              'refresh': 3600, # optional default is 3600 seconds
              # limit to the number of elements to return,
              # not limited if it is 0
              # you can also override it in each source
              'limit': 0, # optional default is 0
           }

    '''

    @classmethod
    def check_config(cls, config):
        if    not 'sources' in config \
           or not isinstance(config['sources'], (tuple, list)) \
           or len(config['sources']) == 0:
               yield 'sources must be a list or a tuple containing at least one element'
        for source in config['sources']:
            if not 'slug' in source:
                yield 'each source must have a slug key'
            if not 'url' in source:
                yield 'each source must have an url key'
            if     'parser_type' in source \
               and source['parser_type'] not in ('raw', 'csv', 'json', 'xml', 'rss'):
                yield 'unknown parser_type {0!r}'.format(source['parser_type'])
            if     'auth_mech' in source:
               if source['auth_mech'] not in ('hmac-sha1', 'hmac-sha256', 'oauth2'):
                   yield 'unknown auth_mech {0!r}'.format(source['auth_mech'])
               if     source['auth_mech'].startswith('hmac-') \
                  and ('signature_key' not in source
                       or not isinstance(source['signature_key'])):
                   yield 'missing signature_key string'

    def get_sources(self, context):
        for source in self.config['sources']:
            slug = '{0}.{1}'.format(self.slug, source['slug'])
            data = Data(slug, self.config, source, context)
            yield source['slug'], data

    def render(self, context):
        for slug, source in self.get_sources(context):
            context[slug] = source
        return context

class Data(object):
    '''Encapsulate data from a source'''

    __CACHE_SENTINEL = object()

    JSON = 'application/json'
    RSS = 'application/rss+xml'
    XML = 'text/xml'
    CSV = 'text/csv'
    OCTET_STREAM = 'application/octet-stream'

    MAPPING = {
            'json': JSON,
            'rss': RSS,
            'xml': XML,
            'csv': CSV,
            'raw': OCTET_STREAM,
    }


    def __init__(self, slug, config, source, context):
        self.slug = slug
        self.context = context
        self.request = context.get('request')
        self.source = source
        self.limit = source.get('limit', config.get('limit', 0))
        self.refresh = source.get('refresh', config.get('refresh', 0))
        self.url = source['url']
        self.verify = source.get('verify_certificate', True)
        self.redirects = source.get('allow_redirects', False)
        self.async = source.get('async', False)
        self.timeout = source.get('timeout', 10)
        self.auth_mech = source.get('auth_mech')
        self.signature_key = source.get('signature_key')
        self.parser_type = source.get('parser_type', 'raw')
        self.content_type = source.get('content_type', self.MAPPING[self.parser_type])
        pre_hash = 'datasource-{self.slug}-{self.url}-{self.limit}-' \
                '{self.refresh}-{self.auth_mech}-{self.signature_key}' \
                .format(self=self)
        self.key = hashlib.md5(pre_hash).hexdigest()
        self.now = time.time()
        self.__content = self.__CACHE_SENTINEL

    def get_oauth2_access_token(self):
        '''Query django-allauth models to find an access token for this user'''
        from allauth.socialaccount.models import SocialToken

        user = self.request.user
        try:
            token = SocialToken.objects.get(
                    account__provider='authentic2',
                    account__user=user)
            log.debug('found access token: %r', token)
            return token.token
        except SocialToken.DoesNotExist:
            log.warning('unable to find a social token for user: %r', user)
            return ''

    def resolve_http_url(self):
        try:
            self.final_url = self.url
            if self.source.get('auth_mech', '').startswith('hmac'):
                # remove the hmac- prefix
                hash_algo = self.auth_mech[:5]
                self.final_url = signature.sign_url(
                        self.final_url,
                        self.signature_key,
                        algo=hash_algo)
            log.debug('getting data source from url %r for renderer %s',
                    self.final_url, self.slug)
            headers = {
                    'Accept': self.content_type,
            }
            if self.auth_mech == 'oauth2':
                headers['Authorization'] = 'Bearer %s' % self.get_oauth2_access_token()
            log.debug('with headers %r', headers)
            request = requests.get(
                    self.final_url,
                    headers=headers,
                    verify=self.verify,
                    allow_redirects=self.redirects,
                    timeout=self.timeout,
                    stream=True)
            request.raise_for_status()
            return request.raw
        except HTTPError:
            log.warning('HTTP Error %s when loading URL %s for renderer %r',
                    request.status_code,
                    self.final_url,
                    self.slug)
        except Timeout:
            log.warning('HTTP Request timeout(%s s) when loading URL '
                    '%s for renderer %s',
                    self.timeout,
                    self.final_url,
                    self.slug)
        except RequestException:
            log.warning('HTTP Request failed when loading URL '
                    '%s for renderer %r',
                    self.final_url,
                    self.slug)

    def resolve_file_url(self):
        path = self.url[7:]
        try:
            return file(path)
        except Exception:
            log.exception('unable to resolve file URL: %r', self.url)

    def update_content(self):
        content = None
        if self.url.startswith('http'):
            stream = self.resolve_http_url()
        elif self.url.startswith('file:'):
            stream = self.resolve_file_url()
        else:
            log.error('unknown scheme: %r', self.url)
            return
        if stream is None:
            return

        data = getattr(self, 'parse_'+self.parser_type)(stream)
        if self.refresh and content is not None:
            cache.set(self.key, (data, self.now+self.refresh), 86400*12)
        log.debug('finished')
        if self.key in self.UPDATE_THREADS:
            c = self.CONDITIONS.setdefault(self.key, threading.Condition())
            with c:
                self.UPDATE_THREADS.pop(self.key)
                self.CONDITIONS.pop(self.key)
        return data

    UPDATE_THREADS = {}
    CONDITIONS = {}

    def get_content(self):
        if self.__content is not self.__CACHE_SENTINEL:
            return self.__content
        self.__content, until = cache.get(self.key, (self.__CACHE_SENTINEL, None))
        use_cache = self.__content is not self.__CACHE_SENTINEL
        # do not use cache if refresh timeout is 0
        use_cache = use_cache and self.refresh > 0
        # do not use cache if updatecache is present in the query string
        use_cache = use_cache and (not self.request or 'updatecache' not in self.request.GET)

        if use_cache:
            if until < self.now:
                # reload cache content asynchronously in a thread
                # and return the current content
                log.debug('stale content reloading')
                c = self.CONDITIONS.setdefault(self.key, threading.Condition())
                t = threading.Thread(target=self.update_content)
                t2 = self.UPDATE_THREADS.setdefault(self.key, t)
                if t2 is t: # yeah we are the first to run
                    with c:
                        t.start()
                        c.notify_all() # notify other updating thread that we started
                if not self.async:
                    if not t2 is t:
                        with c:
                            while not t2.ident:
                                c.wait()
                    t2.join()
        else:
            self.__content = self.update_content()
        return self.__content
    content = property(get_content)

    def parse_json(self, stream):
        import json
        try:
            return json.load(stream)
        except ValueError, e:
            log.exception('unparsable JSON content %s', e)

    def parse_rss(self, stream):
        try:
            result = feedparser.parse(stream.read())
            entries = result.entries
            entries = sorted(result.entries, key=lambda e: e['updated_parsed'])
            result.entries = entries[:self.limit]
            return result
        except Exception, e:
            log.exception('unparsable RSS content %s', e)

    def parse_raw(self, stream):
        return stream.read()

    def parse_xml(self, stream):
        try:
            return ET.fromstring(stream.read())
        except Exception, e:
            log.exception('unparsable XML content', e)

    def parse_csv(self, stream):
        import csv

        try:
            params = self.source.get('csv_params', {})
            encoding = self.source.get('csv_encoding', 'utf-8')

            def list_decode(l):
                return map(lambda s: s.decode(encoding), l)

            def dict_decode(d):
                return dict((a, b.decode(encoding)) for a, b in d.iteritems())

            if hasattr(stream, 'iter_lines'):
                stream = stream.iter_lines()

            if 'fieldnames' in params:
                reader = csv.DictReader(stream, **params)
                decoder = dict_decode
            else:
                reader = csv.reader(stream, **params)
                decoder = list_decode
            return list(decoder(e) for e in reader)
        except Exception, e:
            log.exception('unparsable CSV content')

    def __call__(self):
        return self.get_content()
