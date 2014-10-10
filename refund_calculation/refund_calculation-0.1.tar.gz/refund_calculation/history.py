from __future__ import absolute_import

from collections import namedtuple
from decimal import Decimal

from .windows import Closed, Open


zero = Decimal('0')


class History(namedtuple('History', ('closed', 'open', 'debt'))):

    def __new__(cls, closed=None, open=None, debt=None):
        """
        :param closed: List of Closed
        :param open: List of Open
        :param debt: Decimal
        """
        closed = () if closed is None else tuple(closed)
        open = () if open is None else tuple(open)
        debt = zero if debt is None else Decimal(debt)
        assert debt >= zero
        if debt > zero:
            assert len(open) == 0
        return super(History, cls).__new__(cls, closed, open, debt)

    @property
    def windows(self):
        """
        List of Window, chronological (primarily by start event,
        and secondarily by end event).
        """
        return self.closed + self.open

    def apply(self, event):
        """
        :param event: Event
        :return: History
        """
        return self.step(event.time, event.delta)

    def step(self, time, delta):
        """
        :param time: whatever
        :param delta: Decimal
        :return: History
        """

        # The easiest case - A change of zero is no change at all.
        if delta == zero:
            return self

        # The poorest case - The account is underwater.
        if self.debt > zero:

            # The change is high enough to get us out of debt, and
            # recurse with the remainder.
            if delta > self.debt:
                return self.debt_(lambda x: zero).step(time, delta - self.debt)

            # The change just alters the amount of debt.
            return self.debt_(lambda x: x - delta)

        # An increase creates a new open window.
        if delta > zero:
            return self.open_(lambda x: x + (Open(delta, time),))

        # A decrease is more complicated.

        # If the account is completely zero (neither debt nor balance),
        # the negative delta just takes us into debt.
        if len(self.open) == 0:
            return self.debt_(lambda x: x - delta)

        # The account has some open window. It will be reduced.
        top = self.open[0]

        # If the change consumes the entire top window, convert it
        # into a closed window, and recurse with the remainder.
        if -delta >= top.amount:
            return self.closed_(lambda x: x + (top.close(time),)) \
                .open_(lambda x: x[1:]) \
                .step(time, delta + top.amount)

        # If the top window is greater than the delta, only close
        # part of it.
        return (
            self.closed_(lambda x: x + (
                top.amount_(lambda y: -delta).close(time),
            ))
            .open_(head_(lambda x: x.amount_(lambda y: y + delta)))
        )

    def debt_(self, f):
        return self._replace(debt=f(self.debt))

    def open_(self, f):
        return self._replace(open=f(self.open))

    def closed_(self, f):
        return self._replace(closed=f(self.closed))


def history_from_event_sequence(events):
    h = History()
    for e in events:
        h = h.apply(e)
    return h


def head_(f):
    def g(x):
        return (f(x[0]),) + x[1:]
    return g
