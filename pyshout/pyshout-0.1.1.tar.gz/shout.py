'''
=====
Shout
=====
'''

from __future__ import unicode_literals


__author__ = "Dan Bradham"
__email__ = "danieldbradham@gmail.com"
__version__ = "0.1.1"
__license__ = "MIT"
__description__ = "Loud python messaging!"
__url__ = "http://github.com/danbradham/shout"
__all__ = ["HasEars", "Message", "hears", "shout"]


import inspect
from collections import Sequence, defaultdict
import sys


ROOM_DEFL = "void"


class MetaMsg(type):
    '''Metaclass adding a listeners dict to each subclass allowing them to keep
    track of their own listeners.'''

    def __new__(kls, name, bases, members):

        cls = super(MetaMsg, kls).__new__(kls, name, bases, members)
        cls.listeners = defaultdict(set)

        return cls

MetaMetaMsg = MetaMsg(str("MetaMetaMsg"), (), {}) # 2n3 compatible metaclass

class Message(MetaMetaMsg):
    ''':class:`Message` instances store args and kwargs to shout to their
    listeners. Listeners are any function or class method decorated with
    :func:`hears`. When :meth:`shout` is called these args and kwargs are
    passed to all the listeners that hear the appropriate :class:`Message`
    objects in the appropriate *rooms*. *Rooms* are nothing more than strings
    used as keys in a :class:`Message` object's listeners dictionary. Return
    values of the listeners are collected in the :class:`Message` instance
    results list. If all listeners run successfully the :class:`Message`
    instance success attribute is set to True. If an :class:`Exception` is
    raised during a shout, the shout is stopped and the Exception is bound to
    the :class:`Message` instance exc attribute.

    :param args: Arguments to shout
    :param kwargs: Keyword Arguments to shout
    '''

    def __init__(self, *args, **kwargs):

        try:
            self.room = kwargs.pop("room")
        except KeyError:
            self.room = ROOM_DEFL
        self.args = args
        self.kwargs = kwargs
        self.results = []
        self.exc = None
        self.success = False

    def shout(self):
        '''Sends the :class:`Message` instance args and kwargs to the
        appropriate listeners.'''

        listeners = self.listeners[self.room]
        if not listeners:
            self.exc = UserWarning(
                "Nobody is listening in room: {0}".format(self.room))
            return self

        for listener in listeners:
            try:
                result = listener(*self.args, **self.kwargs)
                self.results.append(result)
            except:
                self.exc = sys.exc_info()[1]
                return self
        self.success = True
        return self

    @classmethod
    def add_listener(cls, fn):
        for room in fn.rooms:
            cls.listeners[room].add(fn)
        return cls

    @classmethod
    def rem_listener(cls, fn):
        for room in cls.listeners.values():
            room.discard(fn)
        return cls

    @staticmethod
    def create(name):
        '''Dynamically create a new :class:`Message` object.

        :param name: The __class__.__name__ to use.
        '''
        message = type(name, (Message,), {})
        return message


class HasEars(object):
    '''A mixin class that automatically takes instance methods decorated with
    :func:`hears` and adds them as listeners to the specified :class:`Message`
    objects.
    '''

    def __init__(self, *args, **kwargs):

        members = inspect.getmembers(self.__class__)
        for name, member in members:
            if getattr(member, "has_ears", False):
                method = getattr(self, member.__name__)
                for msg_type in member.msg_types:
                    msg_type.add_listener(method)
        super(HasEars, self).__init__(*args, **kwargs)


def typecheck_args(args):
    '''Ensures all args are of type Message.'''
    if isinstance(args, Sequence):
        for item in args:
            if not item in Message.__subclasses__():
                raise TypeError(
                    "All arguments passed to hears must be"
                    " subclasses of Message")
        return True

    raise TypeError(
        "Wrong argument signature passed to hears decorator..."
        "Pass a Message subclass or multiple Message subclasses.")


def hears(*args, **kwargs):
    '''A decorator that marks a function or :class:`HasEars` method to hear
    :class:`Message` objects inside specific rooms.

    :param args: A tuple of :class:`Message` objects to hear.
    :param rooms: A tuple of room names to listen to.'''
    def wrapper(fn):

        typecheck_args(args) # Make sure all our args are Message Subclasses

        fn.has_ears = True
        fn.msg_types = args
        fn.rooms = kwargs.get("rooms", (ROOM_DEFL,))

        if isinstance(fn.rooms, str):
            fn.rooms = (fn.rooms,)

        argspec = inspect.getargspec(fn)
        if argspec.args and argspec.args[0] == "self":
            return fn

        for msg_type in fn.msg_types:
            msg_type.add_listener(fn)
        return fn
    return wrapper


def shout(msg_type, *args, **kwargs):
    '''A more grammatically pleasant way to shout a :class:`Message`.

    shout(Message, "Hello", room="A") <==> Message("Hello", room="A").shout()

    :param msg_type: The type of :class:`Message` to shout.
    :param args: The args to pass to the :class:`Message`.
    :param kwargs: The kwargs to pass to the :class:`Message`.
    :param room: The room to shout into.'''
    return msg_type(*args, **kwargs).shout()
