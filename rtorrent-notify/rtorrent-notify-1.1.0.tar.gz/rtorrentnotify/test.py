# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from io import BytesIO
from unittest import TestCase

from rtorrentnotify import Event, Events


class Tests(TestCase):
    def test_db(self):
        maxitems = 20
        db = BytesIO()
        events = Events(db, maxitems)
        events.load()
        for n in range(1, 42):
            events.append(Event('LOL', 'cat %s' % n))
        e = Event('B', 'b')
        events.append(e)
        events.save()

        events = Events(db)
        events.load()
        assert events._events[0].datetime.ctime() == e.datetime.ctime()
        assert len(unicode(events).splitlines()) == maxitems

    def test_add(self):
        events = Events(None)
        events.append(Event('LOL', 'cat'))
        events.append(Event('LOL', 'cat'))
        out = unicode(events)
        assert len(out.splitlines()) == 2

    def test_rss(self):
        events = Events(None)
        events.append(Event('a', 'b'))
        events.append(Event('c', 'héhéhé'))

        feed = events.build_rss()
        out = BytesIO()
        feed.write_xml(out, "utf-8")
        out = out.getvalue().decode('utf-8')
        assert 'guid' in out
