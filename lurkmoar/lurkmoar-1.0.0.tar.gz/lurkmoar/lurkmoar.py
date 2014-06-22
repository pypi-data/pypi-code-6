#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from datetime import datetime
from itertools import imap, repeat
from functools import wraps
from HTMLParser import HTMLParser

import requests

_BASE_URL = "http://a.4cdn.org/"


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
        self._lastfetch = datetime.utcnow()

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
        elif res.status_code == 304:
            return
        else:
            raise requests.HTTPError(res)


class Post(object):
    def __init__(self, post, board, thread):
        self.board = board
        self._thread = thread
        for k, v in post.iteritems():
            if isinstance(v, unicode):
                v = unescape_html(v)
            setattr(self, k, v)

        self._lastfetch = datetime.utcnow()

    def __repr__(self):
        return "<Post> {op.no}, created at {op.now} by {op.name}"

    def _fetch(self):
        self._thread.fetch()

    @update()
    def __getattr__(self, val):
        return getattr(self, val)
