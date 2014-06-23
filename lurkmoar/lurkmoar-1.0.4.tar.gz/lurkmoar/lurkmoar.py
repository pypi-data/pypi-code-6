#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import os
from datetime import datetime
from itertools import imap, repeat
from functools import wraps
from HTMLParser import HTMLParser
from tempfile import mkdtemp

import requests
from PIL import Image

_BASE_URL = "http://a.4cdn.org/"


def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


def unescape_html(string):
    return HTMLParser().unescape(string)


def update(tupdate=10):
    """Decorator that fetches updates for the instance to which the decorated
    method belongs.

    tupdate : int
        Time (in seconds) after which to fetch updates.  Updates will be
        fetched when a decorated method is called.
    """
    def func_wrapper(func):
        @wraps(func)
        def returned_wrapper(self, *args, **kw):
            dt = (datetime.utcnow() - self._lastfetch)
            if dt.total_seconds() > tupdate:
                self._fetch()
            return func(self, *args, **kw)
        return returned_wrapper
    return func_wrapper


class ImageBoardItem(object):
    """Mixin class for `Board` and `Thread`"""
    @update()
    def __iter__(self):
        for item in self._items:
            yield item

    @update()
    def __getitem__(self, val):
        return self._items[val]

    @update()
    def __len__(self):
        return len(self._items)


class Board(ImageBoardItem):
    url = _BASE_URL + "{0}/{page}.json"

    def __init__(self, board, page=1):
        self.board = board
        self._page = page
        self._items = ()

        self._lastfetch = None
        self._fetch(nocache=True)

    def __repr__(self):
        return "<Board> /{0}/, page {1}".format(self.board, self._page)

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value):
        self._page = value
        self._fetch(nocache=True)

    def _get_headers(self, use_if_modified_since=True):
        if use_if_modified_since:
            return {'If-Modified-Since': datetime.utcnow().ctime()}
        return {}

    def _fetch(self, nocache=False):
        """Fetch page listing.

        nocache : bool
            If true, do not use cached values, and instead fetch full page data
            (does **not** use `If-Modified-Since`).
        """
        self._lastfetch = datetime.utcnow()
        hdr = self._get_headers(use_if_modified_since=nocache)
        board = self.url.format(self.board, page=self.page)
        res = requests.get(board, headers=hdr)

        if res.status_code == 200:
            threads = json.loads(res.content)['threads']
            self._items = tuple(imap(Thread, threads, repeat(self.board)))
        elif res.status_code == 304:
            return
        else:
            raise requests.HTTPError(res)


class Thread(ImageBoardItem):
    url = _BASE_URL + "{0}/thread/{1}.json"

    def __init__(self, thread, board):
        self.board = board
        posts = thread['posts']
        self._items = tuple(
            imap(Post, posts, repeat(board), repeat(self))
        )

        self._post_table = {p.no: p for p in self._items}
        self._lastfetch = datetime.utcnow()

        self.tmpdir = mkdtemp(prefix='')

    @classmethod
    def from_id(cls, board, id):
        thread = requests.get(cls.url.format(board, id))
        thread = json.loads(thread)['posts']
        cls(thread, board)

    @update()
    def __repr__(self):
        return "<Thread> OP={op.no}, {op.replies} replies".format(op=self.op)

    @property
    def op(self):
        return self._items[0]

    @property
    def id(self):
        return self.op.no

    @property
    def summary(self):
        summary = """/{op.board}/ thread {op.no}:
        Author: {op.name}
        Created: {op.now}
        OP Replies:  {op.replies}
        Thread Replies: {threadlen}
        Original Post:  {com}  [[{w} characters]]
        """
        return summary.format(op=self.op,
                              com=self.op.com[:50],
                              w=len(self.op.com),
                              threadlen=len(self._items))

    def _fetch(self):
        """Fetch thread updates listing."""
        self._lastfetch = datetime.utcnow()
        hdr = {'If-Modified-Since': datetime.utcnow().ctime()}
        thread = self.url.format(self.board, self.id)
        res = requests.get(thread, headers=hdr)

        if res.status_code == 200:
            posts = json.loads(res.content)['posts']
            self._items = tuple(
                imap(Post, posts, repeat(self.board), repeat(self))
            )
            self._post_table.update({p.no: p for p in self._items})
        elif res.status_code == 304:
            return
        else:
            raise requests.HTTPError(res)


class Post(object):
    _greentext = r"""class="quote">>(?P<greentext>.*)</span>"""
    _link = r"""class="quotelink">>>(?P<greentext>\d+)</a>"""

    def __init__(self, post, board, thread):
        self.board = board
        self._thread = thread

        self._assign_fields(post)

        self._lastfetch = datetime.utcnow()

    def __repr__(self):
        return "<Post> {p.no}, created at {p.now} by {p.name}".format(p=self)

    def _assign_fields(self, post):
        for k, v in post.iteritems():
            if isinstance(v, unicode):
                v = unescape_html(v)
            setattr(self, k, v)

    @property
    def greentext(self):
        greentext = re.findall(self._greentext, getattr(self, 'com', ''))
        return tuple(imap(unicode.strip, greentext))

    @property
    def links(self):
        links = []
        for id in imap(int, re.findall(self._link, self.com)):
            links.append(self._thread._post_table[id])
        return tuple(links)

    def _fetch(self):
        self._thread.fetch()

    @property
    def image(self):
        if not hasattr(self.tim):
            return

        img = 'http://i.4cdn.org/{p.board}/{p.tim}{p.ext}'.format(p=self)
        filename = '{p.tim}{p.ext}'.format(p=self)
        return Post._image(os.path.join(self._thread.tmpdir, filename), img)

    @staticmethod
    @memoize
    def _image(filename, img):
        with open(filename, 'wb') as f:
            f.write(requests.get(img).content)

        img = Image.open(filename)
        os.remove(filename)
        return img
