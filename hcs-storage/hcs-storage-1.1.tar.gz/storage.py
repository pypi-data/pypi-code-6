# -*- coding: UTF-8 -*-
# vim: fileencoding=UTF-8 filetype=python ff=unix et ts=4 sw=4 sts=4 tw=80
#
# Copyright (c) 2010, Christer Sjöholm -- hcs AT furuvik DOT net
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

'''
    >>> s = Storage(a=1)
    >>> d = {}
    >>> s = Storage(a=1, dict_=d)
    >>> d
    {'a': 1}
    >>> s
    Storage(a=1)
    >>> s = Storage(a=1, default_factory=list)
    >>> s.b
    []
    >>> s
    Storage(default_factory=<type 'list'>, a=1, b=[])


    >>> s = Storage(a=1)
    >>> s.A
    Traceback (most recent call last):
    ...
    AttributeError: 'A'
    >>> s = Storage(a=1, B=2, case_insensitive=True)
    >>> s.A
    1
    >>> s.get_dict()
    {'a': 1, 'b': 2}
    >>> s
    Storage(a=1, b=2)

    >>> import binascii
    >>> s = Storage(a='1', B=2, normalize=binascii.hexlify)
    >>> s
    Storage(42=2, 61=u'1')
    >>> s.get_dict()
    {'61': u'1', '42': 2}

    >>> import binascii
    >>> s = Storage(a='1', B=2, normalize=binascii.hexlify, \
                    case_insensitive=True)
    >>> s
    Storage(61=u'1', 62=2)
    >>> s.get_dict()
    {'61': u'1', '62': 2}

    >>> import binascii
    >>> s = Storage(a='1', B=2, normalize=binascii.hexlify, \
                    denormalize=binascii.unhexlify)
    >>> s
    Storage(B=2, a=u'1')
    >>> s.get_contained_dict()
    {'61': u'1', '42': 2}
    >>> s.get_dict()
    {'a': u'1', 'B': 2}


'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections
import json
import six


#    def __init__(self, dict_=None, default_factory=None, normalize=None,
#                 denormalize=None, case_insensitive=False, **kwargs):
class Storage(object):
    """
    A Storage object wraps a dictionary.
    In addition to `obj['foo']`, `obj.foo` can also be used for accessing
    values.

    Wraps the dictionary instead of extending it so that the number of names
    that can conflict with keys in the dict is kept minimal.

        >>> o = Storage(a=1)
        >>> o.a
        1
        >>> o['a']
        1
        >>> 'a' in o
        True
        >>> o.a = 2
        >>> o['a']
        2
        >>> del o.a
        >>> o.a
        Traceback (most recent call last):
            ...
        AttributeError: 'a'

        Based on Storage in web.py (public domain)
    """
    __internal_vars = ('_dict', '_normalize', '_denormalize')

    def __init__(self, dict_=None, default_factory=None, normalize=None,
                 denormalize=None, case_insensitive=False, **kwargs):
        '''
        dict_: Dict to use as backend for Storage object, normalize will not
               be called for existing items.
        case_insensitive: All given keys will be converted to lower case before
                          trying to set/access the dict. If a populated dict_
                          is given it must already have all keys in lower case.
        default_factory: if dict_ is None and default_factory is set then a
                         defaultdict will be used with the specified
                         default_factory.
        normalize: function that normalizes keys, case_insensitive for example
                   is implemented as a normalizer that lower cases each key.
        denormalize: function that is called on each key before it is returned
                     to the caller(iteritems and __iter__).

        '''
        if dict_ is not None:
            self._dict = dict_
        elif default_factory:
            self._dict = collections.defaultdict(default_factory)
        else:
            self._dict = dict()
        if normalize and case_insensitive:
            self._normalize = lambda key: normalize(key.lower())
        elif case_insensitive:
            self._normalize = lambda key: key.lower()
        elif normalize:
            self._normalize = normalize
        else:
            self._normalize = lambda key: key  # Do nothing
        if denormalize:
            self._denormalize = denormalize
        else:
            self._denormalize = lambda key: key  # Do nothing
        for key, value in kwargs.items():
            self[key] = value

    def get_contained_dict(self):
        ''' Get the contained dict.
            all keys will be in their normalized form.
        '''
        return self._dict

    def get_dict(self):
        ''' If there is no denormalize thon get the contained dict otherwise
            return a new list with all keys denormalized.
        '''
        return {self._denormalize(key): val for key, val in self._dict.iteritems()}

    def iteritems(self):
        ''' Iterate over all (key, value) pairs.
        All keys will be denormalized.

        >>> list(Storage(a=1, b=2).iteritems())
        [('a', 1), ('b', 2)]

        '''
        for key, value in self._dict.items():
            yield self._denormalize(key), value

    items = iteritems  # Py3 style

    def __getattr__(self, key):
        '''
        >>> Storage(a=1, b=2).a
        1
        >>> Storage(a=1, b=2).c
        Traceback (most recent call last):
        ...
        AttributeError: 'c'
        >>> Storage(a=1, b=2).__getattr__('_dict')
        Traceback (most recent call last):
        ...
        AttributeError: No such attribute: u'_dict'
        '''
        try:
            # prevent recursion (triggered by pickle.load()
            if key in Storage.__internal_vars:
                raise AttributeError('No such attribute: ' + repr(key))
            key = self._normalize(key)
            return self[key]
        except KeyError as err:
            raise AttributeError(err)

    def __setattr__(self, key, value):
        # prevent recursion (triggered by pickle.load()
        if key in Storage.__internal_vars:
            object.__setattr__(self, key, value)
        else:
            key = self._normalize(key)
            self[key] = value

    def __delattr__(self, key):
        '''
        >>> del Storage(a=1, b=2).a
        >>> del Storage(a=1, b=2).c
        Traceback (most recent call last):
            ...
        AttributeError: 'c'
        '''
        try:
            key = self._normalize(key)
            del self[key]
        except KeyError as err:
            raise AttributeError(err)

    # For container methods pass-through to the underlying dict.
    def __getitem__(self, key):
        key = self._normalize(key)
        return self._dict[key]

    def __setitem__(self, key, value):
        key = self._normalize(key)
        self._dict[key] = value

    def __delitem__(self, key):
        key = self._normalize(key)
        del self._dict[key]

    def __contains__(self, key):
        key = self._normalize(key)
        return key in self._dict

    def __iter__(self):
        for key in self._dict:
            yield self._denormalize(key)

    def __len__(self):
        '''
        >>> len(Storage(a=1, b=2))
        2
        '''
        return self._dict.__len__()

    def __eq__(self, other):
        '''
        >>> Storage(a=1, b=2) == Storage(b=2, a=1)
        True
        >>> Storage(a=1, b=2) == Storage(a=1, b=3)
        False
        '''
        return isinstance(other, Storage) and self._dict == other._dict

    __hash__ = None

    def __repr__(self):
        '''
        >>> repr(Storage(a=1, b=2))
        'Storage(a=1, b=2)'
        '''
        items = []
        if isinstance(self._dict, collections.defaultdict):
            items.append('default_factory={0}'.format(self._dict.default_factory))
        items.extend('{0}={1}'.format(self._denormalize(i[0]), repr(i[1]))
                     for i in sorted(self._dict.items()))
        return '{0}({1})'.format(self.__class__.__name__, ', '.join(items))


def json_loads_storage(str_):
    '''
        >>> json_loads_storage('[{"a":1}]')
        [Storage(a=1)]
    '''
    return json.loads(str_, object_hook=Storage)


def json_load_storage(fp_):
    return json.load(fp_, object_hook=Storage)


def json_dumps_storage(job):
    '''
        >>> json_dumps_storage(Storage(a=2))
        '{\\n  "a": 2\\n}'
        >>> json_dumps_storage([Storage(a=2)])
        '[\\n  {\\n    "a": 2\\n  }\\n]'
        >>> json_dumps_storage({'a':2})
        '{\\n  "a": 2\\n}'
    '''
    return json.dumps(job, default=_storage_to_dict, indent=2)


def json_dump_storage(obj, fp_):
    return json.dump(obj, fp_, default=_storage_to_dict, indent=2)


def _storage_to_dict(obj):
    '''
        >>> _storage_to_dict(Storage(a=1))
        {'a': 1}
        >>> _storage_to_dict('')
        Traceback (most recent call last):
        ...
        TypeError: not a Storage object

    '''
    if isinstance(obj, Storage):
        return obj.get_dict()
    else:
        raise TypeError('not a Storage object')


def unicode_storage(storage):
    '''Convert all values in storage to unicode and assert that all keys
    can be converted

    >>> unicode_storage(Storage(a='b', b=1))
    Storage(a=u'b', b=u'1')
    '''
    for key in storage:
        six.text_type(key)  # just check that it can be done
        storage[key] = six.text_type(storage[key])
    return storage


def storageify(obj, storageFactory=Storage):
    '''
    takes a json style datastructure and converts all dicts to Storage.

    >>> storageify({'a': u'b', 'b': [1, 'c']})
    Storage(a=u'b', b=[1, u'c'])

    '''
    if isinstance(obj, dict):
        res = storageFactory()
        for key, value in obj.items():
            res[key] = storageify(value, storageFactory=storageFactory)
    elif isinstance(obj, list):
        res = []
        for element in obj:
            res.append(storageify(element, storageFactory=storageFactory))
    else:
        res = obj
    return res


def unstorageify(obj):
    '''
    make a deep copy of Storage, dict, and lists
    and convert all Storage to dict
    Good when you want to convert to json or yaml

    >>> unstorageify(Storage(a=u'b', b=[1, 'c', \
                                        [2, 3, Storage(d=4, e={'f': Storage(g=5)})]]))
    {'a': u'b', 'b': [1, u'c', [2, 3, {'e': {u'f': {'g': 5}}, 'd': 4}]]}
    '''
    if isinstance(obj, Storage):
        res = {}
        for key, value in obj.get_dict().items():
            res[key] = unstorageify(value)
    elif isinstance(obj, dict):
        res = {}
        for key, value in obj.items():
            res[key] = unstorageify(value)
    elif isinstance(obj, list):
        res = []
        for element in obj:
            res.append(unstorageify(element))
    else:
        res = obj
    return res
