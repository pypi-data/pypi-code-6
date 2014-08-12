import time
import os
from .encoder import Encoder
from .alphabet import Alphabet

# Should change every year with VERSION
# TODO: Automate it
REDUCE_TIME = 1403265799803
VERSION = 2

class ShortId:

    def __init__(self):
        self._counter = 0
        self._previous_delta = 0
        self._encoder = Encoder()
        self._alphabet = Alphabet()

    def generate(self):
        delta = self._get_time_delta()

        if delta == self._previous_delta:
            self._counter += 1
        else:
            self._counter = 0
            self._previous_delta = delta

        res = self._encoder.encode(self._alphabet.lookup, VERSION)
        res = res + self._encoder.encode(self._alphabet.lookup, os.getpid())

        if self._counter > 0:
            res = res + self._encoder.encode(self._alphabet.lookup, self._counter)

        res = res + self._encoder.encode(self._alphabet.lookup, delta)

        return res

    def _get_time(self):
        return int(time.time() * 1000)

    def _get_time_delta(self):
        return int(round((self._get_time() - REDUCE_TIME) * 0.01))
