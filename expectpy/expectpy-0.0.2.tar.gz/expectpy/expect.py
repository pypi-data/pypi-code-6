import functools


def assertmethod(func):
    """
    instance method decorator.
    Return False, Raise AssertionError.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        res, msg, not_msg = func(self, *args, **kwargs)
        _assert(res, self.negative, msg, not_msg)
    return wrapper


def _assert(res, negative=False, err=None, err_not=None):
    if not negative ^ res:
        msg = err_not if negative else err
        raise AssertionError(msg)


def _error_message(actual, expected, err="", err_not=""):
    return err.format(actual, expected), err_not.format(actual, expected)


class AssertionBuilder:
    chains = [
        "and_", "is_", "not_", "be", "been", "have", "to", "to_not",
        "that", "with", "at", "of", "same", "length_"
    ]

    def __init__(self, obj):
        self._actual = obj
        self.negative = False
        self.is_length = False

    def __getattr__(self, attr):
        if attr in self.chains:
            if attr == "to_not" or attr == "not_":
                self.negative = not self.negative
            elif attr == "length_":
                self.is_length = True
            return self
        raise AttributeError()

    @assertmethod
    def equal(self, expected, err=None):
        err_not = err
        if err is None:
            err, err_not = _error_message(self._actual,
                                          expected,
                                          "expected {0} to equal {1}",
                                          "expected {0} to not equal {1}")
        return self._actual ==  expected, err, err_not

    def eql(self, expected, err=None):
        return self.equal(expected, err)

    @assertmethod
    def a(self, expected, err=None):
        err_not = err
        if err is None:
            err, err_not = _error_message(self._actual,
                                          expected.__name__,
                                          "expected {0} to be a {1}",
                                          "expected {0} to not be a {1}"
                                          )
        return isinstance(self._actual, expected), err, None

    @assertmethod
    def an(self, expected, err=None):
        err_not = err
        if err is None:
            err, err_not = _error_message(self._actual,
                                          expected.__name__,
                                          "expected {0} to be an {1}",
                                          "expected {0} to not be an {1}"
                                          )
        return isinstance(self._actual, expected), err, err_not

    @assertmethod
    def above(self, expected, err=None):
        err_not = err
        actual = len(self._actual) if self.is_length else self._actual
        if err is None:
            err, err_not = _error_message(actual,
                                          expected,
                                          "expected {0} to be above {1}",
                                          "expected {0} to not be above {1}"
                                          )
        return actual > expected, err, err_not

    @assertmethod
    def least(self, expected, err=None):
        err_not = err
        actual = len(self._actual) if self.is_length else self._actual
        if err is None:
            err, err_not = _error_message(actual,
                                          expected,
                                          "expected {0} to be least {1}",
                                          "expected {0} to not be least {1}"
                                          )
        return actual >= expected, err, err_not

    @assertmethod
    def below(self, expected, err=None):
        err_not = err
        actual = len(self._actual) if self.is_length else self._actual
        if err is None:
            err, err_not = _error_message(actual,
                                          expected,
                                          "expected {0} to be below {1}",
                                          "expected {0} to not be below {1}"
                                          )
        return actual < expected, err, err_not

    @assertmethod
    def most(self, expected, err=None):
        err_not = err
        actual = len(self._actual) if self.is_length else self._actual
        if err is None:
            err, err_not = _error_message(actual,
                                          expected,
                                          "expected {0} to be most {1}",
                                          "expected {0} to not be most {1}"
                                          )
        return actual <= expected, err, err_not

    @assertmethod
    def throw(self, error_class, err=None):
        err_not = err
        if err is None:
            err, err_not = _error_message(None, error_class.__name__,
                                          "actual to throw {1}",
                                          "actual to not throw {1}"
                                          )
        try:
            self._actual()
        except error_class:
            return True, err, err_not
        except:
            pass
        return False, err, err_not

    @assertmethod
    def satisfy(self, method, err=None):
        err_not = err
        if err is None:
            err, err_not = _error_message(self._actual,
                                          method.__name__,
                                          "expected {0} to satisfy {1}",
                                          "expected {0} to not satisfy {1}"
                                          )
        return method(self._actual), err, err_not

    @assertmethod
    def within(self, start, finish, err=None):
        err_not = err
        actual = len(self._actual) if self.is_length else self._actual
        if err is None:
            err, err_not = _error_message(actual,
                                          "{0}..{1}".format(start, finish),
                                          "expected {0} to be within {1}",
                                          "expected {0} to not be within {1}"
                                          )
        return start <= actual <= finish, err, err_not

    def string(self, expected, err=None):
        return self.contain(expected, err)

    def include(self, expected, err=None):
        return self.contain(expected, err)

    @assertmethod
    def contain(self, expected, err=None):
        err_not = err
        if err is None:
            err, err_not = _error_message(self._actual,
                                          expected,
                                          "expected {0} to contain {1}",
                                          "expected {0} to not contain {1}"
                                          )
        return expected in self._actual, err, err_not

    @assertmethod
    def match(self, pattern, err=None):
        import re
        err_not = err
        if err is None:
            err, err_not = _error_message(self._actual, pattern,
                                          "expected {0} to match {1}",
                                          "expected {0} to not match {1}"
                                          )
        return True if re.match(pattern, self._actual) else False, err, err_not

    @assertmethod
    def ownProperty(self, name, err=None):
        err_not = err
        if err is None:
            err, err_not = _error_message(self._actual, name,
                                          "expected {0} to have own property {1}",
                                          "expected {0} to not have own property {1}",
                                          )
        return name in self._actual, err, err_not

    def property_(self, name, value=None, err=None):
        if value is None:
            return self.ownProperty(name, err)
        err_not = err
        if err is None:
            err, err_not = _error_message(self._actual,
                                          value,
                                          "expected {0} to equal {1}",
                                          "expected {0} to not equal {1}"
                                          )
        return self._actual[name] == value, err, err_not

    @assertmethod
    def length(self, length, err=None):
        err_not = err
        if err is None:
            err, err_not = _error_message(self._actual,
                                          "{0} but got {1}".format(length, len(self._actual)),
                                          "expected {0} to have a length {1}",
                                          "expected {0} to not have a length {1}"
                                          )
        return len(self._actual) == length, err, err_not

    @property
    def ok(self):
        if not self._actual:
            msg = "expected {0} to be truth".format(self._actual)
            _assert(False, self.negative, msg)
        return self

    @property
    def empty(self):
        # if not empty, assert
        if len(self._actual):
            err = "expected {0} to be empty".format(self._actual)
            err_not = "expected {0} to not be empty".format(self._actual)
            _assert(False, self.negative, err, err_not)
        return self

    @property
    def be_None(self):
        err = "expected {0} to be None".format(self._actual)
        err_not = "expected {0} to not be None".format(self._actual)
        _assert(self._actual is None, self.negative, err, err_not)
        return self

    @property
    def be_True(self):
        err = "expected {0} to be True".format(self._actual)
        err_not = "expected {0} to not be True".format(self._actual)
        _assert(self._actual is True, self.negative, err, err_not)
        return self

    @property
    def be_False(self):
        err = "expected {0} to be False".format(self._actual)
        err_not = "expected {0} to not be False".format(self._actual)
        _assert(self._actual is False, self.negative, err, err_not)
        return self
