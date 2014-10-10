from __future__ import absolute_import

from collections import namedtuple
from decimal import Decimal

from .util import zip


class Event(namedtuple('Event', ('time', 'delta'))):

    def __new__(cls, time, delta):
        delta = Decimal(delta)
        return super(Event, cls).__new__(cls, time, delta)


def make_event_sequence(deltas, times):
    return [Event(time, delta) for time, delta in zip(times, deltas)]
