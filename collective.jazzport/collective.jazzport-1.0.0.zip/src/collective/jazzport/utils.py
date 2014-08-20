# -*- coding: utf-8 -*-
from App.config import getConfiguration
from concurrent import futures
from urllib import urlencode
from urlparse import parse_qs
from urlparse import urlparse
from urlparse import urlunparse
import StringIO
import logging
import os
import re
import requests
import zipfile
import mimetypes

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except ImportError:
    compression = zipfile.ZIP_STORED


types_map = dict([
    (t[1], t[0])
    for t in sorted(mimetypes.types_map.items(), key=lambda t: t[0])
])

logger = logging.getLogger('collective.jazzport')


def ajax_load_url(url):
    scheme, netloc, path, params, query, fragment = urlparse(url)
    query = parse_qs(query)
    query.update({'ajax_load': 1})
    query = urlencode(query)
    return urlunparse([scheme, netloc, path, params, query, fragment])


def get(url, cookies):
    return requests.get(url, cookies=cookies)


def get_canonical_filename(filename):
    keep_characters = ('.', '_', '-')
    return ''.join([c for c in filename.replace(' ', '_')
                    if c.isalnum() or c in keep_characters]).rstrip()


def compress(data):
    keys = sorted(data.keys())
    prefix = keys[0][:keys[0].rfind('/') + 1]

    fb = StringIO.StringIO()
    zf = zipfile.ZipFile(fb, mode='w')

    for url in keys:
        # Get basename
        filename = urlunparse(list(urlparse(url)[:3]) + 3 * [''])[len(prefix):]

        # Get response
        response = data[url]

        # Skip non OK responses
        if response.status_code != 200:
            continue

        # Get suffix from the content-type header
        content_type = \
            (response.headers.get('content-type') or '').split(';')[0]
        if content_type in types_map and not os.path.splitext(filename)[1]:
            filename += types_map.get(content_type)

        # Or get full filename form the content-disposition header
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            for name in re.findall('filename="([^"]+)"', content_disposition):
                filename = filename[:filename.rfind('/') + 1] \
                    + get_canonical_filename(name)
                break

        # Write file top zip
        zf.writestr(filename, response.content)

    zf.close()
    fb.seek(0)

    return fb.read()


class ZipExport(object):

    def __init__(self, filename, urls, **kwargs):
        # (executed within the current Zope worker thread)

        # Read the product config
        product_config = getattr(getConfiguration(),
                                 'product_config', {}) or {}
        configuration = product_config.get('collective.jazzport') or {}
        try:
            self.max_workers = int(configuration.get('max_workers', 5))
        except ValueError:
            self.max_workers = 5

        self.filename = filename
        self.urls = urls
        self.kwargs = kwargs

    def __call__(self, callback):
        # (executed within the exclusive async thread)

        max_workers = self.max_workers
        thread_executor = futures.ThreadPoolExecutor(max_workers=max_workers)

        futures_to_promises = dict([
            (thread_executor.submit(requests.get, url, **self.kwargs), url)
            for url in self.urls
        ])

        data = {}
        for future in futures.as_completed(futures_to_promises):
            url = futures_to_promises[future]
            # noinspection PyBroadException
            try:
                data[url] = future.result()
            except Exception:
                pass

        callback(compress(data), 'application/zip', self.filename)

        thread_executor.shutdown(wait=True)
