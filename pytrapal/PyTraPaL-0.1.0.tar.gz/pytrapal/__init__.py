# -*- coding: UTF-8 -*-
'''\
PyTraPaL – Python Traversal Path Language
=========================================
This project implements a path language to traverse structures of objects in
Python 2 and 3  (tested with CPython 2.7 and 3.3  as well as PyPy 2).
Conceptionally it is inspired by XPath, but uses Python syntax constructs and
operates on Python objects. The primary design goal of the language is defining
concise but short specifications of how select, filter, sort or otherwise
traverse the objects comprising data structures.


Processing Model
----------------
A *path* consists of a arbitrary number of *path steps*; a path step is
comprised of one or more *item selectors*. The path is a callable receiving an
iterable of *initial items* and optionally an environment object and/or an
error handler, returning a :class:`list` of *result items* or :const:`None`,
if there are no result items.

.. productionlist::
    path : `path_step`+
    path_step : `item_selector`+


Item Selectors
^^^^^^^^^^^^^^
An item selector is a callable receiving an iterable of *input items*, the
environment object and the error handler, returning an iterable of *output
items* (possibly empty) or :const:`None`. Thus a path is an item selector
itself.

An item selector must fulfill the following signature:

.. function:: some_module.item_selector(items, env, error_handler)

    :param items: The input items to work on.
    :type items: :class:`list`
    :param env: An arbitrary object which is :const:`None` by default and
        can be set on executing a path.
    :param error_handler: This is a callable with one argument, the exception
        to handle.
    :returns: An iterable of output items or :const:`None`.


Path Execution
^^^^^^^^^^^^^^

When the path is executed (i.e. called), the following is done:

#.  If the input items object is not a :class:`list`, create a :class:`list`
    from the iterable.

#.  Make the list of initial items the *current items list*.

#.  For each path step:

    #.  If the current items list is empty, return it.

    #.  Create an empty :class:`list`, the path step's *next items list*.

    #.  For each item selector of the path step:

        #.  Call the item selector with the current items list.

        #.  Extend the next items list with the items from the iterable
            returned.

    #.  Make the next items list the current items list.

#.  Return the current item list.


Implementation
^^^^^^^^^^^^^^

The following class implements this processing model:

.. autoclass:: Path(*path_steps[, error_handler=logging.exception])
    :special-members: __call__


Decorators
----------

In :mod:`pytrapal` function decorators are defined to make available the item
selectors defined in :mod:`pytrapal.selectors`:

.. function:: use_path(func)

    A function decorator adding to the globals :class:`Path` as well as
    all functions, classes and objects from :mod:`pytrapal.selectors`.

    :param func: The function to modify the globals of.
    :returns: A new function object.

.. autofunction:: use_custom_path


Example
-------

This example shows the features of PyTraPaL and uses the default item
selectors defined in :mod:`pytrapal.selectors`.

We define a path which does the following:

#.  Select all attributes ``data`` from the initial items.
#.  Select the entries ``'foo bar'`` and ``'bar'`` from the mapping object
    items of the previous step.
#.  Create the union of all iterables from the previous step.
#.  Filter the items of the previous step for :class:`str` instances.
#.  Return a sorted list of the items from the previous step.

>>> from pytrapal import Path
>>> from pytrapal.selectors import *
>>> path = Path(Attr.data, (Item['foo bar'], Item.bar), Union,
...     Filter(lambda item: isinstance(item, str)), Sorted())


The following function works similarily and archives the same result:

>>> def manual(items):
...     items = list(items)
...     datas = list()
...     for item in items:
...         try:
...             datas.append(item.data)
...         except AttributeError:
...             pass
...     foo_bars = []
...     for data in datas:
...         try:
...             foo_bars.append(data['foo bar'])
...         except KeyError:
...             pass
...     for data in datas:
...         try:
...             foo_bars.append(data['bar'])
...         except KeyError:
...             pass
...     foo_bar_union = None
...     for foo_bar in foo_bars:
...         try:
...             if foo_bar_union is None:
...                 foo_bar_union = set(foo_bar)
...             else:
...                 foo_bar_union.update(foo_bar)
...         except TypeError:
...             pass
...     if len(foo_bar_union) == 0:
...         return foo_bar_union
...     filtered = filter(lambda item: isinstance(item, str), foo_bar_union)
...     return sorted(filtered)


We define some data structures to apply the path to:

>>> class Test1(object):
...     data = {
...         'foo bar': ['d', 'b', 'a', 'c', 'f'],
...         'bar': (4, 3, 5, 2, 1),
...     }
...
...     @classmethod
...     def foo(cls, index):
...         return cls.data['foo'][index]

>>> class Test2(object):
...     data = {
...         'bar': ('f', 'e', 'g', 'h', 'a'),
...         'foo_bar': {
...             'test': 'foo bar'
...         }
...     }
...
...     @classmethod
...     def bar(cls, key):
...         return cls.data[key]

>>> class Test3(object):
...     value = {
...         't1': Test1,
...         't2': Test2,
...     }


Executing the path is done by calling it with the initial items:

>>> result = path([Test1, Test2, Test3])
>>> print(result)
['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
>>> manual([Test1, Test2, Test3]) == result
True


:mod:`pytrapal.selectors` – Item Selectors for PyTraPaL
-------------------------------------------------------

.. automodule:: pytrapal.selectors
    :no-members:

'''

class Path(object):
    '''\
    Implements the PyTraPaL processing model. Instances are callables
    resolving the path specified on instatiation.

    :param path_steps: The path steps of the path, these may be either
        an item selector or an iterable of those.
    :param error_handler: If there is a named parameter `error_handler` this
        will be the default error handler for the instance. Otherwise the
        default error handler is :func:`logging.exception`.
    :raises ValueError: If no path step is supplied.
    '''
    def __init__(self, *path_steps, **kargs):
        if len(path_steps) == 0:
            raise ValueError('No path steps given.')
        execution_path_steps = []
        for path_step in path_steps:
            try:
                execution_path_steps.append(tuple(path_step))
            except TypeError:
                execution_path_steps.append((path_step,))
        self._path_steps = tuple(execution_path_steps)
        if 'error_handler' in kargs:
            self._default_error_handler = kargs['error_handler']

    from logging import exception as _default_error_handler

    def __call__(self, items, env=None, error_handler=None):
        '''\
        Executes the path with the given items as the input items.

        :param items: An iterable of the input items.
        :param env: An arbitrary object.
        :param error_handler: The error handler to use. If this is
            :const:`None` the default error handler will be used.
        :returns: a :class:`list` of the output items.
        '''
        if error_handler is None:
            error_handler = self._default_error_handler
        if not isinstance(items, list):
            items = list(items)
        current = items
        for path_step in self._path_steps:
            next = []
            for path_item in path_step:
                try:
                    path_item_result = path_item(current, env=env,
                        error_handler=error_handler)
                    next.extend(path_item_result)
                except Exception as e:
                    error_handler(e)
            if len(next) == 0:
                return next
            else:
                current = next
        return current


def _path_dict():
    path_dict = dict()
    from pytrapal import selectors
    for name in dir(selectors):
        if not name.startswith('_'):
            path_dict[name] = getattr(selectors, name)
    path_dict['Path'] = Path
    return path_dict

_path_dict = _path_dict()

from tinkerpy import update_globals as _update_globals

use_path = _update_globals(**_path_dict)


def use_custom_path(**additional_entries):
    '''\
    Creates a function decorator like :func:`use_path`, but with the globals
    updated additionally with the items from ``additional_entries``.

    :param additional_entries: The items to add additionally to the globals.
    :returns: The function decorator created.
    '''
    path_dict = dict(_path_dict)
    path_dict.update(additional_entries)
    return _update_globals(**path_dict)
