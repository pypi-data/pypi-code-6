"""
Python based enumartion type

Usage Example
=============
    >>> Colors = Enum("Red","Yellow","Blue")
    >>> print Colors.Red
    0
    >>> print Colors.Yellow
    1
    >>> print 2 == Colors.Blue
    True
    >>> print Colors.names[2]
    Blue
    >>> print Colors.names.index('Blue')
    2
    
"""
from functools import partial
__all__ = ['Enum']

def has_key(enum, key):
    return key in enum.keys()

def get_key(enum, value):
    keys = [k for k, v in enum.iteritems() if v == value]
    if len(keys) > 1:
        raise ValueError('Multiple keys have value {0}, this method is unusable'.format(value))
    return keys[0]

def Enum(*enumerated):
    #If only a dictionary is passed to enum it means we are making up our own values
    #otherwise just enumerate the given list of keys
    if len(enumerated) == 1 and isinstance(enumerated[0], dict):
        enums = enumerated[0]
    else:
        enums = dict(zip(enumerated, range(len(enumerated))))
    
    enums['get_key'] = partial(get_key, enums)
    enums['has_key'] = partial(has_key, enums)
    return type('Enum', (), enums)

if __name__ == "__main__":
    print "here"
    Colors = Enum("Red","Yellow","Blue")
    print Colors.Red
    print Colors.Yellow
    print 2 == Colors.Blue
    print Colors.names[2]
    print Colors.names.index('Blue')

