from enum import IntEnum


class ParseError(Exception):
    pass


class Metrics(object):
    DEFAULT = None
    _NO_VALUE = object()

    def __init__(self, filename):
        self.filename = filename
        self._mapping = self._NO_VALUE

    def as_mapping(self):
        if self._mapping is self._NO_VALUE:
            self._mapping = self.calculate_mapping()
        return self._mapping

    def __getattr__(self, name):
        return getattr(self.as_mapping(), name)


class Metric(object):
    def __init__(self, value):
        self.value = value

    def compared_to(other):
        raise NotImplementedError

    def __str__(self):
        return str(self.value)


class Severity(IntEnum):
    low = 1
    medium = 2
    high = 3
