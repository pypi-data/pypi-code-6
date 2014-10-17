#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import time
from drove.data.event import Event
from nose.tools import raises


def test_event():
    """Testing Event: dump()"""
    event = Event("example", "CRITICAL", "message",
                  nodename="test", timestamp=0)
    assert event.dump() == "E|0|test|example|CRITICAL|message"

    event = Event("example", "CRITICAL", "message", nodename="test")
    assert event.dump() == ("E|%d|test|example|CRITICAL|message" %
                            (int(time.time()),))


def test_event_dump():
    """Testing Event: from_dump()"""
    event = Event.from_dump("E|0|test|example|CRITICAL|message")
    assert event.dump() == "E|0|test|example|CRITICAL|message" == repr(event)


@raises(ValueError)
def test_event_malformed():
    """Testing Event: malformed event"""
    Event.from_dump("E|0")
