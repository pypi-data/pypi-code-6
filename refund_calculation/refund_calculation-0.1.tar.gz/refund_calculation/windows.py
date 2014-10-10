from __future__ import absolute_import

from collections import namedtuple
from decimal import Decimal


class Window(object):

    def amount_(self, f):
        return self._replace(amount=f(self.amount))


class Closed(namedtuple('Closed', ('amount', 'start', 'end')), Window):

    def __new__(cls, amount, start, end):
        amount = Decimal(amount)
        assert amount > 0
        return super(Closed, cls).__new__(cls, amount, start, end)


class Open(namedtuple('Open', ('amount', 'start')), Window):

    def __new__(cls, amount, start):
        amount = Decimal(amount)
        assert amount > 0
        return super(Open, cls).__new__(cls, amount, start)

    def close(self, end):
        return Closed(self.amount, self.start, end)

    @property
    def end(self):
        return None
