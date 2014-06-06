__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"


def load(function):
    """
    This decorator checking of the class was loaded and load it if needed.
    For lazy.
    Needs attribute _is_loaded and a function reload().
    """
    def _load_wrapper(self, *args):
        if not self._is_loaded:
            self.reload()
        return function(self, *args)
    return _load_wrapper


def my_load(function):
    """
    This decorator checking of the class was loaded and load it if needed.
    For lazy.
    Needs attribute _is_my_loaded and a function my_reload().
    """
    def _my_load_wrapper(self, *args):
        if not self._is_my_loaded:
            self.my_reload()
        return function(self, *args)
    return _my_load_wrapper


class Singleton(type):
    """
    Singleton.
    
    Returns:
        An existsing instance.
    """
    _instances = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonFactory(type):
    """
    Singleton Factory - keeps one object with the same hash
        of the same cls.
    
    Returns:
        An existing instance.
    """
    __instances = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = dict()
        new_obj = super(SingletonFactory, cls).__call__(*args, **kwargs)
        if hash(new_obj) not in cls.__instances[cls]:
            cls.__instances[cls][hash(new_obj)] = new_obj
        return cls.__instances[cls][hash(new_obj)]

    def _unregiter(cls, obj):
        cls.__instances[cls].pop(hash(obj))
