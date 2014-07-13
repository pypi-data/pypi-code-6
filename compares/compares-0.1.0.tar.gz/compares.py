try:
    import reprlib
except ImportError:
    import repr as reprlib


__version__ = "0.1.0"


def via(fields):
    """
    Define the fields (attributes) to use for instance comparison and repr.

    Creates ``__eq__``\ , ``__ne__`` and ``__repr__`` methods for the
    decorated class, along with a private ``_contents`` property which
    simply returns the fields provided with associated values on the
    instance, and a ``fields`` attribute simply containing the fields.

    Other than ``__eq__`` and ``__ne__`` any existing attributes will be
    untouched if already defined on the class.

    :argument iterable fields: the names of attributes that should be
        considered relevant for comparison and display. The order that the
        iterable returns the fields in affects the order in which comparison
        happens and the order they are displayed in the ``__repr__``\ .

    """

    def add_methods(cls):
        nothing = object()

        if getattr(cls, "fields", nothing) is nothing:
            cls.fields = tuple(fields)

        def contents(self):
            return [(attr, getattr(self, attr)) for attr in fields]

        if getattr(cls, "_contents", nothing) is nothing:
            cls._contents = property(contents)

        def __eq__(self, other):
            if not isinstance(other, self.__class__):
                return NotImplemented
            return contents(self) == contents(other)
        cls.__eq__ = __eq__

        def __ne__(self, other):
            if not isinstance(other, self.__class__):
                return NotImplemented
            return not self == other
        cls.__ne__ = __ne__

        if cls.__repr__ == object.__repr__:
            def __repr__(self):
                fields_repr = " ".join(
                    "{0}={1}".format(k, reprlib.repr(v))
                    for k, v in contents(self)
                )
                return "<{0.__class__.__name__} {1}>".format(self, fields_repr)
            cls.__repr__ = __repr__

        return cls
    return add_methods
