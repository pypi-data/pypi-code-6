"""
    jsonspec.pointer.exceptions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

__all__ = ['ExtractError', 'RefError', 'LastElement', 'OutOfBounds', 'OutOfRange', 'WrongType']


class ExtractError(Exception):
    """Raised for any errors.

    :ivar obj: the object that raised this event
    """

    def __init__(self, obj, *args):
        super(ExtractError, self).__init__(*args)
        self.obj = obj


class RefError(ExtractError):
    """Raised when encoutered a JSON Ref.

    :ivar obj: the object that raised this event
    """


class WrongType(ExtractError, ValueError):
    """Raised when a member or a sequence is needed.

    :ivar obj: the object that raised this event
    """


class OutOfBounds(ExtractError, KeyError):
    """Raised when a member of a mapping does not exists.

    :ivar obj: the object that raised this event
    """


class OutOfRange(ExtractError, IndexError):
    """Raised when an element of a sequence does not exists.

    :ivar obj: the object that raised this event
    """


class LastElement(ExtractError):
    """Raised when refers to the last element of a sequence.

    :ivar obj: the object that raised this event
    """
