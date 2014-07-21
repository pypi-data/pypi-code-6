""" Main ReBASE module

:Author: peter1000
:Github: https://github.com/peter1000
:Copyright: (c) 2014 All Rights Reserved

**All `ReBASE classes - subclasses`**:

   .. warning:: for all `ReBASE classes` disabled methods

      - any class.copy()

         - e.g.: xy = myrlist.copy()

      - any class.clear()

         - e.g.: myrlist.clear()

      - any __setattr__()
      - any __delattr__()
      - any __add__()

   - can be dumped with json: but will lose any extra data like: `key_order (list)` or/and any `extra_data dict`
   - can be pickled

   - additional methods:

      - set_extra_data(), update_extra_data(), replace_extra_data(): Sets/updates key/value to the additional dictionary: `extra_data`

      - copy_recursively(): recursively copy: Supports recursively intermediate ReDICT, ReLIST, ReTUPLE, dicts, lists and tuples (and their subclasses: depending on there implementation though)

         - this will also copy any ReDICT / ReLIST / ReTUPLE / ReMATRIX `extra_data dict` and any `key_order (list)` and any `extra_key_order (list)`

      - copy_recursively_to_python_native_types(): recursively copy: changing all `ReOBJ` to native python types.

         - `RdictIO, RdictFO, RdictFO2: to python `OrderedDict obj` keeping their order (see also argument: use_extra_key_order)

         - all other ReDICT: objects will be replaced by normal python `dict objs`
         - all `ReLIST obj` will be replaced by normal python `list objs`
         - all `ReTUPLE obj` will be replaced by normal python `tuple objs`
         - all `ReMATRIX obj` will be replaced by normal python `list of tuple objs`

            .. warning::  ReMATRIX tuple items (rows) are not recursively copied so there should be no dict, list ect.. just basic types

         Supports recursively intermediate ReDICT, ReLIST, ReTUPLE, dicts, lists and tuples (and their subclasses: depending on there implementation though)

         .. note:: any ReOBJ set: `extra_data` will be lost

      - topickle(): returns a new pickled dumps byte string from the obj

      - tojson(): returns a new json dumps string from the obj

      - tojson_keeporder(): returns a new json dumps string from the obj keeping the order of any `RdictIO, RdictFO, RdictFO2`

         - this uses first the: copy_recursively_to_python_native_types()

.. warning:: comparisons do not take into consideration any `key_order (list)` or `extra_data dict`
"""
from collections import OrderedDict
from copy import deepcopy
from json import dumps as jdumps
from pickle import (
   dumps as pdumps,
   loads as ploads
)

from ReOBJ.ProjectErr import (
   MethodDeactivatedErr,
   Err
)


class ReBase(object):
   """ Common Base of ReOBJ

   Raises
      MethodDeactivatedErr, KeyError, AttributeError, ReOBJ.ProjectErr.Err
   """

   def set_extra_data(self, key, value):
      """ Sets/updates key/value to the additional dictionary: `extra_data`

      In subclasses which use and init which sets always `extra_data` this method should be overwritten removing the: if
      """
      if 'extra_data' not in self.__dict__:
         self.__dict__['extra_data'] = {}
      self.__dict__['extra_data'][key] = value

   def update_extra_data(self, new_extra_data_dict):
      """ Updates/Extends the additional dictionary: `extra_data`

      In subclasses which use and init which sets always `extra_data` this method should be overwritten removing the: if
      """
      if 'extra_data' not in self.__dict__:
         self.__dict__['extra_data'] = {}
      self.__dict__['extra_data'].update(new_extra_data_dict)

   def replace_extra_data(self, new_extra_data_dict):
      """ Replaces the `extra_data (dict)` with the dict

      if extra_data did not exist it will be created

      Args:
         new_extra_data_dict (dict):
      """
      self.__dict__['extra_data'] = new_extra_data_dict

   def copy_recursively(self):
      """ Create a recursively copy of the ReOBJ obj

      - copy_recursively(): recursively copy: Supports recursively intermediate ReDICT, ReLIST, ReTUPLE, dicts, lists and tuples (and their subclasses: depending on there implementation though)

         - this will also copy any ReDICT / ReLIST / ReTUPLE / ReMATRIX `extra_data dict` and any `key_order (list)` and any `extra_key_order (list)`

      Returns:
         obj: copy of the ReOBJ

            - all ReOBJ are copied inclusive any set: `extra_data`
      """

      def inner_copy(input_):
         if isinstance(input_, RdictIO):
            temp_new = type(input_)([(key, inner_copy(input_[key])) for key in input_.key_order], input_.use_tuple_values)
            temp_new.__dict__['extra_key_order'] = input_.extra_key_order.copy()
            temp_new.__dict__['extra_data'] = input_.extra_data.copy()
            # key_order / extra_data: no need to copy that separately it is done at __init__
            return temp_new
         elif isinstance(input_, (Rdict, Edict)):
            temp_new = type(input_)((key, inner_copy(value)) for key, value in input_.items())
            if 'extra_data' in input_.__dict__:
               temp_new.__dict__['extra_data'] = input_.extra_data.copy()
            return temp_new
         elif isinstance(input_, (Rlist, Elist, Etuple)):
            temp_new = type(input_)([inner_copy(value) for value in input_])
            if 'extra_data' in input_.__dict__:
               temp_new.__dict__['extra_data'] = input_.extra_data.copy()
            return temp_new
         elif isinstance(input_, Lmatrix):
            temp_new = type(input_)(input_.column_names, [tuple_row for tuple_row in input_], input_.unique_column_names)
            temp_new.__dict__['extra_data'] = input_.extra_data.copy()
            # column_names, column_names_idx_lookup, column_names_counted: no need to copy that separately it is done at __init__
            return temp_new
         elif isinstance(input_, dict):
            return type(input_)((key, inner_copy(value)) for key, value in input_.items())
         elif isinstance(input_, (list, tuple)):
            return type(input_)([inner_copy(value) for value in input_])
         else:
            return deepcopy(input_)

      return inner_copy(self)


   def copy_recursively_to_python_native_types(self, use_extra_key_order=False):
      """ Return a recursively copy: changing all `ReOBJ` to native python types.

      - `RdictIO, RdictFO, RdictFO2: to python `OrderedDict obj` keeping their order (see also argument: use_extra_key_order)

      - all other ReDICT: objects will be replaced by normal python `dict objs`
      - all `ReLIST obj` will be replaced by normal python `list objs`
      - all `ReTUPLE obj` will be replaced by normal python `tuple objs`
      - all `ReMATRIX obj` will be replaced by normal python `list of tuple objs`

      Supports recursively intermediate ReDICT, ReLIST, ReTUPLE, dicts, lists and tuples (and their subclasses: depending on there implementation though)

      .. note:: any ReOBJ set: `extra_data` will be lost

      Args:
         use_extra_key_order (bool):

            - if True: the OrderedDict will be based on the `extra_key_order (list)`
            - if False: it will be base on the default `key_order (list)`

      Returns:
         obj: recursive copy of the obj with ReOBJs replaced by python native objs
      """

      def inner_copy(input_):
         if isinstance(input_, RdictIO):
            if use_extra_key_order:
               return OrderedDict([(key, inner_copy(input_[key])) for key in input_.extra_key_order])
            else:
               return OrderedDict([(key, inner_copy(input_[key])) for key in input_.key_order])
         elif isinstance(input_, (Rdict, Edict)):
            return dict((key, inner_copy(value)) for key, value in input_.items())
         elif isinstance(input_, (Rlist, Elist)):
            return list(inner_copy(value) for value in input_)
         elif isinstance(input_, Lmatrix):
            return [tuple(tuple_row) for tuple_row in input_]
         elif isinstance(input_, Etuple):
            return tuple([inner_copy(value) for value in input_])
         elif isinstance(input_, dict):
            return type(input_)((key, inner_copy(value)) for key, value in input_.items())
         elif isinstance(input_, (list, tuple)):
            return type(input_)([inner_copy(value) for value in input_])
         else:
            return deepcopy(input_)

      return inner_copy(self)

   def topickle(self):
      """ Returns a new pickled dumps byte string from the obj

      Returns:
         bytes: a pickled `ReOBJ` dumps
      """
      return pdumps(self, protocol=4)

   def tojson(self, ensure_ascii=False, indent='   '):
      """ Returns a new json dumps string from the obj

      Args:
         ensure_ascii (bool):

            - If ensure_ascii is True, the output is guaranteed to have all incoming non-ASCII characters escaped.
            - If ensure_ascii is False, these characters will be output as-is.

         indent():
            If indent is a non-negative integer or string, then JSON array elements and object members will be pretty-printed with that indent level.
            An indent level of 0, negative, or "" will only insert newlines.
            None (the default) selects the most compact representation.
            Using a positive integer indent indents that many spaces per level.
            If indent is a string (such as "\t"), that string is used to indent each level.

      Returns:
         bytes: a pickled `ReOBJ` dumps
      """
      return jdumps(self, ensure_ascii=ensure_ascii, indent=indent)

   def tojson_keeporder(self, use_extra_key_order=False, ensure_ascii=False, indent='   '):
      """ Returns a new json dumps string from the obj keeping the order using first: copy_recursively_to_python_native_types()

      - `RdictIO, RdictFO, RdictFO2`: will keep their order (see also argument: use_extra_key_order)

      Args:
         use_extra_key_order (bool):

            - if True: the OrderedDict will be based on the `extra_key_order (list)`
            - if False: it will be base on the default `key_order (list)`

         ensure_ascii (bool):

            - If ensure_ascii is True, the output is guaranteed to have all incoming non-ASCII characters escaped.
            - If ensure_ascii is False, these characters will be output as-is.

         indent():
            If indent is a non-negative integer or string, then JSON array elements and object members will be pretty-printed with that indent level.
            An indent level of 0, negative, or "" will only insert newlines.
            None (the default) selects the most compact representation.
            Using a positive integer indent indents that many spaces per level.
            If indent is a string (such as "\t"), that string is used to indent each level.

      Returns:
         bytes: a pickled `ReOBJ` dumps
      """
      temp_native_with_order = self.copy_recursively_to_python_native_types(use_extra_key_order=use_extra_key_order)
      return jdumps(temp_native_with_order, ensure_ascii=ensure_ascii, indent=indent)

   # DEACTIVATED
   @staticmethod
   def deactivated_(*args, **kwargs):
      """ Helper method used to raise MethodDeactivatedErr
      """
      raise MethodDeactivatedErr()

   clear = deactivated_
   copy = deactivated_
   __setattr__ = deactivated_
   __delattr__ = deactivated_
   __add__ = deactivated_


# ================================== R/E DICTS ================================== #
class Edict(ReBase, dict):
   """ An extended dictionary: E(xtended) like a normal python dict but with the additional methods of the `ReBase class`

   Raises
      ReOBJ.ProjectErr.Err
   """

   @staticmethod
   def frompickle(in_pickle_dumps):
      """ Create a new `Edict` from a pickled dumps.

      Arg:
         in_pickle_dumps (bytes): a pickled `Edict` dumps

      Returns:
         obj: a new Rdict object
      """
      new_obj = ploads(in_pickle_dumps)
      if not isinstance(new_obj, Edict):
         raise Err('Edict.frompickle()', 'Error: `in_pickle_dumps` does not seem to be a base `Edict` object: Got type: <{}>'.format(type(new_obj)))
      return new_obj


class Rdict(ReBase, dict):
   """ A restricted dictionary:

   - new keys **can** be added
   - item values **can** be changed
   - item **can not** be deleted

   Raises
      MethodDeactivatedErr, KeyError, AttributeError, ReOBJ.ProjectErr.Err
   """

   @staticmethod
   def frompickle(in_pickle_dumps):
      """ Create a new `Rdict` from a pickled dumps.

      Arg:
         in_pickle_dumps (bytes): a pickled `Rdict` dumps

      Returns:
         obj: a new Rdict object
      """
      new_obj = ploads(in_pickle_dumps)
      if not isinstance(new_obj, Rdict):
         raise Err('Rdict.frompickle()', 'Error: `in_pickle_dumps` does not seem to be a base `Rdict` object: Got type: <{}>'.format(type(new_obj)))
      return new_obj

   @classmethod
   def fromkeys(cls, key_name_list, value=None):
      """ Create a new `Rdict` with keys from *key_name_list* and values set to *value*.

      Arg:
         key_name_list (list): a list with key names
         value (any): each item will be set to the same initial value

      Returns:
         obj: a new Rdict object
      """
      return cls([(key, value) for key in key_name_list])

   def __reduce__(self):
      """ Return state information for pickling
      """
      items = [(key, self[key]) for key in self]
      inst_dict = self.__dict__.copy()
      if inst_dict:
         return (self.__class__, (items,), inst_dict)
      return self.__class__, (items,)

   # DEACTIVATED
   __delitem__ = ReBase.deactivated_  # NOTE: Speedtest: defining __delitem__ is the main slowdown for adding new items: additional 100% more time
   setdefault = ReBase.deactivated_
   pop = ReBase.deactivated_
   popitem = ReBase.deactivated_
   update = ReBase.deactivated_


class RdictF(Rdict):
   """ A restricted dictionary: F(ix)

   Similar to `Rdict` but after creation/initialization no new keys can be added
   There are some other differences too.

   - can **only** be initialized but is `fix` afterwards
   - new keys **can not** be added
   - item values **can** be changed
   - item **can not** be deleted

   Raises
      MethodDeactivatedErr, KeyError, AttributeError, ReOBJ.ProjectErr.Err
   """

   def __setitem__(self, key, value):
      """ Called to implement assignment to self[key].

      Restriction: after RdictF creation no new keys can be set.

      Raises:
         KeyError: if `key` is not found
      """
      if key in self:
         dict.__setitem__(self, key, value)
      else:
         raise KeyError('RdictF.__setitem__(): <{}> object has no attribute: <{}>'.format(type(self).__name__, key))

   @staticmethod
   def frompickle(in_pickle_dumps):
      """ Create a new `RdictF` from a pickled dumps.

      Arg:
         in_pickle_dumps (bytes): a pickled `RdictF` dumps

      Returns:
         obj: a new RdictF object
      """
      new_obj = ploads(in_pickle_dumps)
      if not isinstance(new_obj, RdictF):
         raise Err('RdictF.frompickle()', 'Error: `in_pickle_dumps` does not seem to be a base `RdictF` object: Got type: <{}>'.format(type(new_obj)))
      return new_obj

   # DEACTIVATED
   get = ReBase.deactivated_


class RdictIO(Rdict):
   """ A restricted dictionary: I(nsertion) O(rder)

   Similar to `Rdict` but the order of the keys insertion are tracked in a list: `key_order`
   There are some other differences too.

   - new keys **can** be added
   - item values **can** be changed

      .. note:: keep in mind that values might be tuples: depending ont `tuple_values`

   - item **can not** be deleted

   Args:
      list_of_key_value_tuples (list): of tuples

         - first tuple item is: dict key
         - other tuple item

            - depends on `tuple_values` setting

      use_tuple_values: bool

         - if True: output will be a tuple with all values except the first (dict key)

            - Example with single values

               .. code-block:: python

                  rdictio_obj = RdictIO2([
                     ('jack', 4098),
                     ('hair', 'brown'),
                     ('eyes', 'blue'),
                  ], True)

                  # output tuples
                  rdictio_obj:  {'eyes': ('blue',), 'jack': (4098,), 'hair': ('brown',)}


            - this is usually used with multiple values tuples like

               .. code-block:: python

                  rdictio_obj = RdictIO2([
                     ('jack', 4098, 'dummy_func'),
                     ('hair', 'brown', 'dummy_func'),
                     ('eyes', 'blue', 'dummy_func'),
                  ], True)

                  # output tuples
                  rdictio_obj:  {'eyes': ('blue', 'dummy_func'), 'hair': ('brown', 'dummy_func'), 'jack': (4098, 'dummy_func')}


         - if False: the first (dict key), the second will be the value

            - only used with key-value-pair tuples like in a `normal python dict`

               .. code-block:: python

                  rdictio_obj = RdictIO2([
                     ('jack', 4098),
                     ('hair', 'brown'),
                     ('eyes', 'blue'),
                  ], False)

                  # output
                  rdictio_obj:  {'hair': 'brown', 'eyes': 'blue', 'jack': 4098}

      init_extra_key_order (bool):

         - if True: the `extra_key_order (list)` will be initialize with a copy of the `key_order (list)`
         - if False: the `extra_key_order (list)` will be an empty list

   Raises
      MethodDeactivatedErr, KeyError, AttributeError, ReOBJ.ProjectErr.Err
   """

   def __init__(self, key_value_list, use_tuple_values, init_extra_key_order=True):
      """ Initializes RdictIO
      """
      if isinstance(key_value_list, list):
         if use_tuple_values:
            dict.__init__(self, {key_value_tuple[0]: key_value_tuple[1:] for key_value_tuple in key_value_list})
         else:
            dict.__init__(self, {key: value for key, value in key_value_list})

         self.__dict__['key_order'] = [item[0] for item in key_value_list]
         if init_extra_key_order:
            self.__dict__['extra_key_order'] = self.key_order.copy()
         else:
            self.__dict__['extra_key_order'] = []
         self.__dict__['extra_data'] = {}
         self.__dict__['use_tuple_values'] = use_tuple_values
      else:
         raise Err('RdictIO.__init__()', 'key_value_list must be a list of key/value pairs: We got type: <{}>\n   <{}>'.format(type(key_value_list), key_value_list))

   def __setitem__(self, key, value):
      """ Called to implement assignment to self[key].

      NOTE: Speedtest: defining __setitem__ is the main slowdown
      """
      if key not in self:
         self.__dict__['key_order'].append(key)
      dict.__setitem__(self, key, value)

   def set_extra_data(self, key, value):
      """ Sets/updates key/value to the additional dictionary: `extra_data`
      """
      self.__dict__['extra_data'][key] = value

   def update_extra_data(self, new_extra_data_dict):
      """ Updates/Extends the additional dictionary: `extra_data`
      """
      self.__dict__['extra_data'].update(new_extra_data_dict)

   def yield_key_value_order(self):
      """ Returns a generator: (keys, values) over the `key_order (list)`

      Yields:
         (keys, value) in the order of the `key_order (list)`
      """
      for key in self.key_order:
         yield key, self[key]

   def yield_extra_key_value_order(self):
      """ Returns a generator: (keys, values) over the `extra_key_order (list)`

      Yields:
         (keys, value) in the order of the `extra_key_order (list)`
      """
      for key in self.extra_key_order:
         yield key, self[key]

   def replace_extra_key_order(self, new_extra_key_order_list):
      """ Replaces the `extra_key_order (list)` with the new_extra_key_order

      - Checks that each key is also in the default: `key_order (list)`

      Args:
         new_extra_key_order_list (list): user defined keys order (may be also just a subset of the RdictIO keys)

      Raises:
         ReOBJ.Err: if any key from new_extra_key_order is not found in the default `key_order (list)`
      """
      for key in new_extra_key_order_list:
         if key not in self.key_order:
            raise Err('RdictIO.replace_extra_key_order()', 'Error: `new_extra_key_order_list` key: <{}>\n  was not found in the default `key_order (list)`:\n    <{}>'.format(key, self.key_order))
      self.__dict__['extra_key_order'] = new_extra_key_order_list

   def appendto_extra_key_value_order(self, new_key):
      """ Appends the `new_key` with the the user defined `extra_key_order (list)`

      - Checks that each key is also in the default: `key_order (list)`

      Args:
         new_key (obj): append a new key to the user defined keys order (may be also just a subset of the RdictIO keys)

      Raises:
         ReOBJ.Err: if the `new_key` is not found in the default `key_order (list)`
      """
      if new_key not in self.key_order:
         raise Err('RdictIO.replace_extra_key_order()', 'Error: new_key: <{}>\n  was not found in the default `key_order (list)`:\n    <{}>'.format(new_key, self.key_order))
      self.__dict__['extra_key_order'].append(new_key)

   def __reduce__(self):
      """ Return state information for pickling
      """
      items = [(key, self[key]) for key in self]
      inst_dict = self.__dict__.copy()
      inst_use_tuple_values = self.use_tuple_values
      return (self.__class__, (items, inst_use_tuple_values,), inst_dict)

   @staticmethod
   def frompickle(in_pickle_dumps):
      """ Create a new `RdictIO` from a pickled dumps.

      Arg:
         in_pickle_dumps (bytes): a pickled `RdictIO` dumps

      Returns:
         obj: a new RdictIO object
      """
      new_obj = ploads(in_pickle_dumps)
      if not isinstance(new_obj, RdictIO):
         raise Err('RdictIO.frompickle()', 'Error: `in_pickle_dumps` does not seem to be a base `RdictIO` object: Got type: <{}>'.format(type(new_obj)))
      return new_obj

   # DEACTIVATED
   fromkeys = ReBase.deactivated_


class RdictFO(RdictIO):
   """ A restricted dictionary: F(ix) O(rder)

   Similar to `RdictIO` but after creation/initialization no new keys can be added
   There are some other differences too.

   - can **only** be initialized but is `fix` afterwards: `key_order list` has the key order as in the `key_value_list argument`
   - new keys **can not** be added
   - item values **can** be changed

      .. note:: keep in mind that values might be tuples: depending ont `tuple_values`

   - item **can not** be deleted

   for arguments see: RdictIO()

   Raises
      MethodDeactivatedErr, KeyError, AttributeError, ReOBJ.ProjectErr.Err
   """

   def __setitem__(self, key, value):
      """ Called to implement assignment to self[key].

      Restriction: after RdictFO creation no new keys can be set.

      Raises:
         KeyError: if `key` is not found
      """
      if key in self:
         dict.__setitem__(self, key, value)
      else:
         raise KeyError('RdictFO.__setitem__(): <{}> object has no attribute: <{}>'.format(type(self).__name__, key))

   @staticmethod
   def frompickle(in_pickle_dumps):
      """ Create a new `RdictFO` from a pickled dumps.

      Arg:
         in_pickle_dumps (bytes): a pickled `RdictFO` dumps

      Returns:
         obj: a new RdictFO object
      """
      new_obj = ploads(in_pickle_dumps)
      if not isinstance(new_obj, RdictFO):
         raise Err('RdictFO.frompickle()', 'Error: `in_pickle_dumps` does not seem to be a base `RdictFO` object: Got type: <{}>'.format(type(new_obj)))
      return new_obj

   # DEACTIVATED
   get = ReBase.deactivated_


class RdictFO2(RdictFO):
   """ A restricted dictionary: F(ix) O(rder)

   Similar to `RdictFO` but after creation/initialization values can not be changed

   - can **only** be initialized but is `fix` afterwards: `key_order list` has the key order as in the `key_value_list argument`
   - new keys **can not** be added
   - item values **can not** be changed
   - item **can not** be deleted

   for arguments see: RdictIO()

   Raises
      MethodDeactivatedErr, KeyError, AttributeError, ReOBJ.ProjectErr.Err
   """

   @staticmethod
   def frompickle(in_pickle_dumps):
      """ Create a new `RdictFO2` from a pickled dumps.

      Arg:
         in_pickle_dumps (bytes): a pickled `RdictFO2` dumps

      Returns:
         obj: a new RdictFO2 object
      """
      new_obj = ploads(in_pickle_dumps)
      if not isinstance(new_obj, RdictFO2):
         raise Err('RdictFO2.frompickle()', 'Error: `in_pickle_dumps` does not seem to be a base `RdictFO2` object: Got type: <{}>'.format(type(new_obj)))
      return new_obj

   # DEACTIVATED
   __setitem__ = ReBase.deactivated_


# ================================== R/E LISTS ================================== #
class Elist(ReBase, list):
   """ An extended list: E(xtended) like a normal python list but with the additional methods of the `ReBase class`

   Raises
      ReOBJ.ProjectErr.Err
   """

   @staticmethod
   def frompickle(in_pickle_dumps):
      """ Create a new `Elist` from a pickled dumps.

      Arg:
         in_pickle_dumps (bytes): a pickled `Elist` dumps

      Returns:
         obj: a new Elist object
      """
      new_obj = ploads(in_pickle_dumps)
      if not isinstance(new_obj, Elist):
         raise Err('Elist.frompickle()', 'Error: `in_pickle_dumps` does not seem to be a base `Elist` object: Got type: <{}>'.format(type(new_obj)))
      return new_obj


class Rlist(ReBase, list):
   """ A restricted list:

   - new items **can** be added
   - item values **can** be changed
   - item **can not** be deleted

   Raises
      MethodDeactivatedErr, ReOBJ.ProjectErr.Err
   """

   @staticmethod
   def frompickle(in_pickle_dumps):
      """ Create a new `Rlist` from a pickled dumps.

      Arg:
         in_pickle_dumps (bytes): a pickled `Rlist` dumps

      Returns:
         obj: a new Rlist object
      """
      new_obj = ploads(in_pickle_dumps)
      if not isinstance(new_obj, Rlist):
         raise Err('Rlist.frompickle()', 'Error: `in_pickle_dumps` does not seem to be a base `Rlist` object: Got type: <{}>'.format(type(new_obj)))
      return new_obj

   # DEACTIVATED
   __delitem__ = ReBase.deactivated_
   pop = ReBase.deactivated_
   remove = ReBase.deactivated_


class RlistF(Rlist):
   """ A restricted list: F(ix)

   Similar to `Rlist` but after creation/initialization no new items can be added
   There are some other differences too.

   - can **only** be initialized but is `fix` afterwards
   - new items **can not** be added
   - item values **can** be changed
   - item **can not** be deleted

   Raises
      MethodDeactivatedErr, ReOBJ.ProjectErr.Err
   """

   @staticmethod
   def frompickle(in_pickle_dumps):
      """ Create a new `RlistF` from a pickled dumps.

      Arg:
         in_pickle_dumps (bytes): a pickled `RlistF` dumps

      Returns:
         obj: a new RlistF object
      """
      new_obj = ploads(in_pickle_dumps)
      if not isinstance(new_obj, RlistF):
         raise Err('RlistF.frompickle()', 'Error: `in_pickle_dumps` does not seem to be a base `RlistF` object: Got type: <{}>'.format(type(new_obj)))
      return new_obj

   # DEACTIVATED
   append = ReBase.deactivated_
   extend = ReBase.deactivated_
   insert = ReBase.deactivated_


# ================================== R/E TUPLES ================================== #
class Etuple(ReBase, tuple):
   """ An extended tuple: E(xtended) like a normal python tuple but with the additional methods of the `ReBase class`

   Raises
      ReOBJ.ProjectErr.Err
   """

   @staticmethod
   def frompickle(in_pickle_dumps):
      """ Create a new `Etuple` from a pickled dumps.

      Arg:
         in_pickle_dumps (bytes): a pickled `Etuple` dumps

      Returns:
         obj: a new Etuple object
      """
      new_obj = ploads(in_pickle_dumps)
      if not isinstance(new_obj, Etuple):
         raise Err('Etuple.frompickle()', 'Error: `in_pickle_dumps` does not seem to be a base `Etuple` object: Got type: <{}>'.format(type(new_obj)))
      return new_obj


# ================================== R/E MATRIX ================================== #
def _helper_find_duplicates(seq):
   """ Helper Returns a list of duplicates
   """
   seen = {}
   seen_twice = {}
   for item in seq:
      if item in seen:
         seen_twice[item] = None
      else:
         seen[item] = None
   return seen_twice.keys()


class Lmatrix(ReBase, list):
   """ An extended MATRIX (List-Of-Tuples): E(xtended) with the additional methods of the `ReBase class`

   Tuple items (rows) should only be simple objects: no nested list, dictionary: this is not enforces but not all other methods support such:

      e.g.: copy_recursively_to_python_native_types()

   Arg:
      column_names (tuple): strings of column names
      list_tuple__of_tuples (list or tuple): items (tuples - rows) must have the same number of values as there are column_names
      unique_column_names (bool): if True all column names must be unique: some methods require this

   Raises
      ReOBJ.ProjectErr.Err
   """

   def __init__(self, column_names, list_tuple__of_tuples, unique_column_names=True):
      """ Initializes Lmatrix
      """
      if isinstance(list_tuple__of_tuples, (list, tuple)):
         if isinstance(column_names, tuple):
            if unique_column_names:
               if len(column_names) != len(set(column_names)):
                  raise Err('Lmatrix.__init__()', 'Seems that not all column names are unique: Problems: <{}>\n   column_names: <{}>'.format(_helper_find_duplicates(column_names), column_names))

            list.__init__(self, list_tuple__of_tuples)

            self.__dict__['column_names'] = column_names
            self.__dict__['column_names_idx_lookup'] = {key: idx for idx, key in enumerate(column_names)}
            self.__dict__['column_names_counted'] = len(column_names)
            self.__dict__['extra_data'] = {}
            self.__dict__['unique_column_names'] = unique_column_names
         else:
            raise Err('Lmatrix.__init__()', 'column_names must be a tuple: We got type: <{}>\n   <{}>'.format(type(column_names), column_names))

      else:
         raise Err('Lmatrix.__init__()', 'list_tuple__of_tuples must be a `list or tuple of tuples`: We got type: <{}>\n   <{}>'.format(type(list_tuple__of_tuples), list_tuple__of_tuples))


   def set_extra_data(self, key, value):
      """ Sets/updates key/value to the additional dictionary: `extra_data`
      """
      self.__dict__['extra_data'][key] = value

   def update_extra_data(self, new_extra_data_dict):
      """ Updates/Extends the additional dictionary: `extra_data`
      """
      self.__dict__['extra_data'].update(new_extra_data_dict)

   def replace_column_names(self, new_column_names_tuple):
      """ Replaces the `column_names (tuple)` with the new_column_names_tuple

      Args:
         new_column_names_tuple (tuple): must have the same number of names as the current `column_names`

      Raises:
         ReOBJ.Err
      """
      if isinstance(new_column_names_tuple, tuple):
         if len(new_column_names_tuple) == self.column_names_counted:
            self.__dict__['column_names'] = new_column_names_tuple
            self.__dict__['column_names_idx_lookup'] = {key: idx for idx, key in enumerate(new_column_names_tuple)}
            return
      raise Err('Lmatrix.replace_column_names()', 'new_column_names_tuple must be a <tuple> with: <{}> column_names: We got type: <{}>\n   <{}>'.format(self.__dict__['column_names_counted'], type(new_column_names_tuple), new_column_names_tuple))


   def this_column_values(self, column_name):
      """ Returns the items of all rows for the column

      Arg:
         column_name (string):

      Returns:
         list: all items of the column for all rows
      """
      if column_name in self.column_names:
         idx = self.column_names_idx_lookup[column_name]
         return [row[idx] for row in self]
      else:
         raise Err('Lmatrix.this_column_values()', 'column_name: <{}> is not a valid one.\n   Registered names: <{}>'.format(column_name, self.column_names))


   def __setitem__(self, idx, row_tuple):
      """ Called to implement assignment to self[idx].

      Arg:
         row_tuple (tuple): tuple must have the same number of items as: the original `tuple_column_names`

      Raises:
         IndexError:: if out of `idx`
      """
      if isinstance(row_tuple, tuple):
         if len(row_tuple) == self.column_names_counted:
            list.__setitem__(self, idx, row_tuple)
            return
      raise Err('Lmatrix.__setitem__()', 'item to append must be a <tuple> with: <{}> items: We got type: <{}>\n   <{}>'.format(self.__dict__['column_names_counted'], type(row_tuple), row_tuple))


   def append(self, row_tuple):
      """ Append row_tuple

      Arg:
         row_tuple (tuple): tuple must have the same number of items as: the original `tuple_column_names`
      """
      if isinstance(row_tuple, tuple):
         if len(row_tuple) == self.column_names_counted:
            list.append(self, row_tuple)
            return
      raise Err('Lmatrix.append()', 'item to append must be a <tuple> with: <{}> items: We got type: <{}>\n   <{}>'.format(self.__dict__['column_names_counted'], type(row_tuple), row_tuple))

   def insert(self, idx, row_tuple):
      """ Insert row_tuple

      Arg:
         idx (int): where to insert
         row_tuple (tuple): tuple must have the same number of items as: the original `tuple_column_names`
      """
      if isinstance(row_tuple, tuple):
         if len(row_tuple) == self.column_names_counted:
            list.insert(self, idx, row_tuple)
            return
      raise Err('Lmatrix.insert()', 'item to insert must be a <tuple> with: <{}> items: We got type: <{}>\n   <{}>'.format(self.__dict__['column_names_counted'], type(row_tuple), row_tuple))


   def extend(self, other_matrix):
      """ Extend row_tuple

      Arg:
         other_matrix: must have same number of column names
      """
      if isinstance(other_matrix, Lmatrix):
         if other_matrix.__dict__['column_names_counted'] == self.column_names_counted:
            list.extend(self, other_matrix)
            return
      raise Err('Lmatrix.extend()', 'item to extend must be a <Lmatrix or Subclass> with: <{}> column names: We got type: <{}>\n   column_names_counted: <{}>\n    rows: <{}>'.format(self.__dict__['column_names_counted'], type(other_matrix), other_matrix.__dict__['column_names_counted'], other_matrix))


   @staticmethod
   def frompickle(in_pickle_dumps):
      """ Create a new `Lmatrix` from a pickled dumps.

      Arg:
         in_pickle_dumps (bytes): a pickled `Lmatrix` dumps

      Returns:
         obj: a new Lmatrix object
      """
      new_obj = ploads(in_pickle_dumps)
      if not isinstance(new_obj, Lmatrix):
         raise Err('Lmatrix.frompickle()', 'Error: `in_pickle_dumps` does not seem to be a base `Lmatrix` object: Got type: <{}>'.format(type(new_obj)))
      return new_obj


class LmatrixF(Lmatrix):
   """ A restricted MATRIX (List-Of-Tuples): F(ix)

   Similar to `Lmatrix` but after creation/initialization no new items can be added
   There are some other differences too.

   This is quite similar to using a Tuple-of-Tuples: but we keep it a subclass of Lmatrix

   - can **only** be initialized but is `fix` afterwards
   - new items (tuple-rows) **can not** be added
   - item (tuple-rows) **can not** be changed / replaced
   - item (tuple-rows) **can not** be deleted

   Tuple items should only be simple objects: no nested list, dictionary: this is not enforces but not all other methods support such:

      e.g.: copy_recursively_to_python_native_types()

   Arg:
      column_names (tuple): strings of column names
      list_tuple__of_tuples (list or tuple): items (tuples - rows) must have the same number of values as there are column_names
      unique_column_names (bool): if True all column names must be unique: some methods require this

   Raises
      ReOBJ.ProjectErr.Err
   """

   @staticmethod
   def frompickle(in_pickle_dumps):
      """ Create a new `LmatrixF` from a pickled dumps.

      Arg:
         in_pickle_dumps (bytes): a pickled `LmatrixF` dumps

      Returns:
         obj: a new LmatrixF object
      """
      new_obj = ploads(in_pickle_dumps)
      if not isinstance(new_obj, LmatrixF):
         raise Err('LmatrixF.frompickle()', 'Error: `in_pickle_dumps` does not seem to be a base `LmatrixF` object: Got type: <{}>'.format(type(new_obj)))
      return new_obj

   # DEACTIVATED
   __delitem__ = ReBase.deactivated_
   __setitem__ = ReBase.deactivated_
   pop = ReBase.deactivated_
   remove = ReBase.deactivated_

   append = ReBase.deactivated_
   extend = ReBase.deactivated_
   insert = ReBase.deactivated_
