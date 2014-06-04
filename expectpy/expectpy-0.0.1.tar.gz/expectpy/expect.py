import functools


def assertmethod(func):
    """
    instance method decorator.
    Return False, Raise AssertionError.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        if hasattr(self, "err"):
            _assert(res, self.negative, self.err)
        else:
            _assert(res, self.negative)
    return wrapper


def _assert(res, negative=False, err=None):
    if not negative ^ res:
        if err:
            raise AssertionError(err)
        else:
            raise AssertionError()


class AssertionBuilder:
    chains = [
        "and_", "is_", "not_", "be", "been", "have", "to", "to_not",
        "that", "with", "at", "of", "same", "length_"
    ]

    def __init__(self, val):
        self.actual = val
        self.negative = False
        self.is_length = False

    def __getattr__(self, attr):
        if attr in self.chains:
            if attr == "to_not" or attr == "not_":
                self.negative = True
            elif attr == "length_":
                self.is_length = True
            return self
        raise AttributeError()

    @assertmethod
    def equal(self, expected):
        return self.actual == expected

    @assertmethod
    def a(self, expected):
        return isinstance(self.actual, expected)

    @assertmethod
    def an(self, expected):
        return isinstance(self.actual, expected)

    @assertmethod
    def above(self, expected):
        actual = len(self.actual) if self.is_length else self.actual
        return actual > expected

    @assertmethod
    def least(self, expected):
        actual = len(self.actual) if self.is_length else self.actual
        return actual >= expected

    @assertmethod
    def below(self, expected):
        actual = len(self.actual) if self.is_length else self.actual
        return actual < expected

    @assertmethod
    def most(self, expected):
        actual = len(self.actual) if self.is_length else self.actual
        return actual <= expected

    @assertmethod
    def throw(self, err):
        try:
            self.actual()
        except err:
            return True
        except:
            pass
        return False

    @assertmethod
    def satisfy(self, method):
        return method(self.actual)

    @assertmethod
    def within(self, start, finish):
        actual = len(self.actual) if self.is_length else self.actual
        return start <= actual <= finish

    @assertmethod
    def string(self, string):
        return string in self.actual

    @assertmethod
    def include(self, value):
        return value in self.actual

    @assertmethod
    def contain(self, value):
        return value in self.actual

    @assertmethod
    def match(self, pattern):
        import re
        return True if re.match(pattern, self.actual) else False

    @assertmethod
    def ownProperty(self, name):
        return name in self.actual

    @assertmethod
    def property_(self, name, value):
        return self.actual[name] == value

    @assertmethod
    def length(self, length):
        return len(self.actual) == length

    @property
    def ok(self):
        if not self.actual:
            _assert(False, self.negative)
        return self

    @property
    def empty(self):
        # if not empty, assert
        if len(self.actual):
            _assert(False, self.negative)
        return self

    @property
    def be_None(self):
        _assert(self.actual is None, self.negative)
        return self

    @property
    def be_True(self):
        _assert(self.actual is True, self.negative)
        return self

    @property
    def be_False(self):
        _assert(self.actual is False, self.negative)
        return self
