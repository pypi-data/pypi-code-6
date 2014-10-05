import collections
import abc

__version__ = '0.4'

DEFAULT_FLAG_NAME = '_is_loaded'
DEFAULT_FUNCTION_NAME = 'reload'


class ReloadedSet(collections.Set, metaclass=abc.ABCMeta):
    """
    A reloaded set - like frozenset but can fetch new data in the function reload.
    To inheritance you need to make:

    :ivar _values: The value the set will look when doing staff.
    :type _values: any things that can be iterable like list, tuple, set or frozen set.
    :ivar _is_loaded: The flag that will check that the object is first load or not.
    :type _is_loaded: bool
    """
    def __init__(self, flag_name: str=DEFAULT_FLAG_NAME, function_name: str=DEFAULT_FUNCTION_NAME):
        setattr(self, flag_name, False)

        inner_function_name = '_' + function_name

        @abc.abstractmethod
        def function():
            getattr(self, inner_function_name)()
            setattr(self, flag_name, True)
        setattr(self, function_name, function)

    @property
    @abc.abstractmethod
    def _values(self):
        pass

    def __contains__(self, item):
        return item in self._values

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def issubset(self, other) -> bool:
        return frozenset(self) <= frozenset(other)

    def issuperset(self, other) -> bool:
        return frozenset(self) >= frozenset(other)

    def union(self, *others) -> frozenset:
        return frozenset(self).union(*others)

    def __or__(self, other) -> frozenset:
        return self.union(other)

    def intersection(self, *others) -> frozenset:
        return frozenset(self).intersection(*others)

    def __and__(self, other) -> frozenset:
        return self.intersection(other)

    def difference(self, *others) -> frozenset:
        return frozenset(self).difference(*others)

    def __sub__(self, other) -> frozenset:
        return self.difference(other)

    def symmetric_difference(self, other) -> frozenset:
        return frozenset(self).symmetric_difference(other)

    def __xor__(self, other) -> frozenset:
        return self.symmetric_difference(other)


def load(flag_name: str=DEFAULT_FLAG_NAME, function_name: str=DEFAULT_FUNCTION_NAME):
    """
    This decorator checking of the class was loaded and load it if needed.
    For lazy.
    """
    def _decorator_wrapper(function):
        """
        The real decorator
        :param function: The function to wrap.
        :return: The wrapped function.
        """
        def _load_wrapper(self, *args):
            flag = getattr(self, flag_name)
            if not flag:
                reload_function = getattr(self, function_name)
                reload_function()
            return function(self, *args)

        return _load_wrapper

    return _decorator_wrapper