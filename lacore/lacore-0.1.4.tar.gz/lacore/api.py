from urlparse import urljoin
from lacore import get_client_info
from lacore.decorators import cached_property, contains
from lacore.async import deferred_property, block
from lacore.exceptions import (ApiAuthException, UploadEmptyError,
                               ApiUnavailableException, ApiErrorException)
from lacore.date import parse_timestamp
from lacore.log import getLogger
from twisted.internet import defer
from twisted.python import failure

import json
import treq

from twisted.web.client import HTTPClientFactory
HTTPClientFactory.noisy = True


class TwistedRequestsFactory(object):
    def __init__(self):
        pass

    class TreqSession(object):
        auth = None
        verify = None
        user_agent = None

    class TwistedRequestsSession(object):
        defaults = {
            'persistent': False
        }

        def __init__(self, session):
            self.session = session
            if session.user_agent is not None:
                ua = session.user_agent
            else:
                ua = get_client_info()
            self.defaults.setdefault('headers', {}).update({
                'User-Agent': [str(ua)]})

        @defer.inlineCallbacks
        def get_content(self, r):
            if r.code == 401:
                yield failure.Failure(ApiAuthException())
            if r.code == 404:
                yield failure.Failure(ApiUnavailableException())
            if r.code > 300:
                yield failure.Failure(ApiErrorException(
                    " ".join([str(r.code), str(r.phrase)])))
            r = yield treq.content(r)
            defer.returnValue(json.loads(r))

        def _defaults(self, kwds):
            defaults = {}
            defaults.update(self.defaults)
            defaults.update(kwds)
            return defaults

        @defer.inlineCallbacks
        def maybeauth(self, method, *args, **kwargs):
            try:
                r = yield method(*args, **self._defaults(kwargs))
                r = yield self.get_content(r)
            except ApiAuthException:
                kwargs['auth'] = self.session.auth
                r = yield method(*args, **self._defaults(kwargs))
                r = yield self.get_content(r)
            defer.returnValue(r)

        def get(self, *args, **kwargs):
            return self.maybeauth(treq.get, *args, **kwargs)

        def post(self, *args, **kwargs):
            return self.maybeauth(treq.post, *args, **kwargs)

        def patch(self, *args, **kwargs):
            return self.maybeauth(treq.patch, *args, **kwargs)

    def __call__(self, prefs={}):
        session = self.TreqSession()
        if 'user' in prefs and 'pass' in prefs:
            session.auth = (prefs['user'], prefs['pass'])
        if 'verify' in prefs:
            session.verify = prefs['verify']
        if 'user_agent' in prefs:
            session.user_agent = prefs['user_agent']
        return Api(prefs, self.TwistedRequestsSession(session))


RequestsFactory = TwistedRequestsFactory()


class UploadState(object):
    def __init__(self, archive, size, uri=None, capsule=None, sandbox=False):
        self.archive = archive
        self.size = size
        self.capsule = capsule
        self.sandbox = sandbox
        self.uri = uri


class UploadOperation(object):
    uri = None

    def __init__(self, api, archive, state):
        self.archive = archive
        self.capsule = state.capsule
        self.api = api
        self.uri = state.uri
        self.sandbox = state.sandbox

    @defer.inlineCallbacks
    def start(self):
        endpoints = yield self.api.endpoints
        data = json.dumps({
            'title': self.archive.title,
            'description': self.archive.description or '',
            'capsule': self.capsule['resource_uri'],
            'size': self.archive.meta.size,
            'sandbox': self.sandbox
        })
        r = yield self.api._post(endpoints['upload'], data=data)
        self.uri = urljoin(self.api.url, r['resource_uri'])
        defer.returnValue(self.api.parse_status(r))

    @defer.inlineCallbacks
    def poll(self):
        r = yield self.api._get(self.uri)
        defer.returnValue(self.api.parse_status(r))

    @property
    def status(self):
        if self.uri is None:
            d = self.start()
        else:
            d = self.poll()
        d.addErrback(
            lambda f: getLogger().debug(
                "Exception while getting status", exc_info=True) or f)
        return d

    def finalize(self, auth=None, keys=[]):
        if self.uri is None:
            raise UploadEmptyError(
                reason="Attempt to finalize upload that hasn't started")
        patch = {'status': 'uploaded', 'size': self.archive.meta.size,
                 'parts': len(keys)}
        if auth is not None:
            patch['checksums'] = {}
            if hasattr(auth, 'sha512'):
                patch['checksums']['sha512'] = auth.sha512.encode("hex")
            if hasattr(auth, 'md5'):
                patch['checksums']['md5'] = auth.md5.encode("hex")
        return self.api._patch(self.uri, data=json.dumps(patch))


class Api(object):

    def __init__(self, prefs, session=None):
        self.url = prefs.get('url')
        self.prefs = prefs
        self.session = session

    @deferred_property
    def root(self):
        r = yield self._get(self.url)
        defer.returnValue(r)

    @deferred_property
    def endpoints(self):
        root = yield self.root
        r = yield dict(((n, urljoin(self.url, r['list_endpoint']))
                       for n, r in root.iteritems()))
        defer.returnValue(r)

    @defer.inlineCallbacks
    def _get(self, url):
        r = yield self.session.get(url.encode('utf8'))
        defer.returnValue(r)

    @defer.inlineCallbacks
    def _data(self, url, method, data=None):
        headers = {}
        if data is not None:
            headers['content-type'] = 'application/json'
        r = yield method(
            url.encode('utf8'), headers=headers, data=data)
        defer.returnValue(r)

    def _post(self, url, data=None):
        return self._data(url, self.session.post, data)

    def _patch(self, url, data=None):
        return self._data(url, self.session.patch, data)

    def upload(self, archive, state):
        op = UploadOperation(self, archive, state)
        return op

    def upload_cancel(self, state):
        pass

    @defer.inlineCallbacks
    def get_endpoint(self, name):
        endpoints = yield self.endpoints
        url = endpoints[name]
        r = yield self._get(url)
        defer.returnValue(r)

    @defer.inlineCallbacks
    def async_capsules(self):
        r = yield self.get_endpoint('capsule')
        defer.returnValue(self.capsule_list(r))

    def capsules(self):
        return block(self.async_capsules)()

    @contains(list)
    def object_list(self, os, kwds=None, tstamps=[]):
        for o in os.get('objects'):
            ret = dict([(k, o.get(k, None)) for k in kwds])
            for kw in tstamps:
                ret[kw] = parse_timestamp(ret[kw])
            yield ret

    def capsule_list(self, cs):
        ks = ['title', 'remaining', 'size', 'id', 'resource_uri',
              'created', 'expires']
        return self.object_list(cs, kwds=ks, tstamps=['created', 'expires'])

    @contains(dict)
    def capsule_ids(self, size=None):
        for capsule in self.capsules():
            if size is None or capsule['remaining'] >= size:
                yield (capsule['id'], capsule)

    @defer.inlineCallbacks
    def async_archives(self):
        r = yield self.get_endpoint('archive')
        defer.returnValue(self.archive_list(r))

    def archives(self):
        return block(self.async_archives)()

    def archive_list(self, ars):
        ks = ['capsule', 'description', 'size', 'key', 'resource_uri',
              'created', 'expires', 'title']
        return self.object_list(ars, kwds=ks, tstamps=['created', 'expires'])

    @deferred_property
    def async_account(self):
        r = yield self.get_endpoint('account')
        defer.returnValue(r)

    @cached_property
    @block
    def account(self):
        return self.async_account

    @defer.inlineCallbacks
    def upload_status_async(self, uri):
        r = yield self._get(uri)
        defer.returnValue(self.parse_status(r))

    @block
    def upload_status(self, uri):
        return self.upload_status_async(uri)

    def parse_status(self, rsp):
        if rsp:
            if 'created' in rsp:
                rsp['created'] = parse_timestamp(rsp['created'])
            if 'expires' in rsp:
                rsp['expires'] = parse_timestamp(rsp['expires'])
            if 'archive' in rsp:
                rsp['archive'] = urljoin(self.url, rsp['archive'])
        return rsp
# vim: et:sw=4:ts=4
