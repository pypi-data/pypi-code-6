__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"


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
