# Copyright 2014 Ray Harris

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this module except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import unicode_literals

from .util import *

__all__ = ['Insist']


class Insist(object):

  def __init__(self, error_type=AssertionError, message_prefix=None, always_show_standard=False):

    if not exception_class(error_type):
      raise TypeError('Value for error_type must be a class derived from Exception')

    if not string_or_none(message_prefix):
      raise TypeError('Value for message_prefix must be a string or None')

    if not isinstance(always_show_standard, bool):
      raise TypeError('Value for always_show_standard must be a bool')

    self._type = error_type

    self._prefix = message_prefix

    self._both = always_show_standard


  def _message(self, standard, custom):
    if self._both and custom:
      message = '{} : {}'.format(custom, standard)
    elif custom:
      message = custom
    else:
      message = standard

    if self._prefix:
      message = '{} : {}'.format(self._prefix, message)

    return message


  def __call__(self, expr, custom=None):
    if not isinstance(expr, bool):
      raise TypeError('Value for expr must be a bool')

    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not expr:
      msg = 'Expression is False instead of True'
      raise self._type(self._message(msg, custom))


  def true(self, expr, custom=None):
    if not isinstance(expr, bool):
      raise TypeError('Value for expr must be a bool')

    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not expr:
      msg = 'Expression is False instead of True'
      raise self._type(self._message(msg, custom))


  def false(self, expr, custom=None):
    if not isinstance(expr, bool):
      raise TypeError('Value for expr must be a bool')

    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if expr:
      msg = 'Expression is True instead of False'
      raise self._type(self._message(msg, custom))


  def equal(self, first, second, custom=None):
    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not (first == second):
      msg = '{} == {} fails'.format(first, second)
      raise self._type(self._message(msg, custom))


  def not_equal(self, first, second, custom=None):
    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not (first != second):
      msg = '{} != {} fails'.format(first, second)
      raise self._type(self._message(msg, custom))


  def less(self, first, second, custom=None):
    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not (first < second):
      msg = '{} < {} fails'.format(first, second)
      raise self._type(self._message(msg, custom))


  def less_equal(self, first, second, custom=None):
    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not (first <= second):
      msg = '{} <= {} fails'.format(first, second)
      raise self._type(self._message(msg, custom))


  def greater(self, first, second, custom=None):
    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not (first > second):
      msg = '{} > {} fails'.format(first, second)
      raise self._type(self._message(msg, custom))


  def greater_equal(self, first, second, custom=None):
    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not (first >= second):
      msg = '{} >= {} fails'.format(first, second)
      raise self._type(self._message(msg, custom))


  def is_same(self, first, second, custom=None):
    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not (first is second):
      msg = '{} is {} fails'.format(first, second)
      raise self._type(self._message(msg, custom))


  def is_not(self, first, second, custom=None):
    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not (first is not second):
      msg = '{} is not {} fails'.format(first, second)
      raise self._type(self._message(msg, custom))


  def is_in(self, first, second, custom=None):
    if not is_iterable(second):
      raise TypeError('Second value must be an iterable object')

    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not (first in second):
      msg = '{} in {} fails'.format(first, second)
      raise self._type(self._message(msg, custom))


  def not_in(self, first, second, custom=None):
    if not is_iterable(second):
      raise TypeError('Second value must be an iterable object')

    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not (first not in second):
      msg = '{} not in {} fails'.format(first, second)
      raise self._type(self._message(msg, custom))


  def is_subclass(self, first, second, custom=None):
    if not is_class(first):
      raise TypeError('First value must be a class')

    if not class_or_tuple(second):
      raise TypeError('Second value must be a class or tuple of classes')

    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not issubclass(first, second):
      first = class_names(first)
      second = class_names(second)
      msg = '{} is not a subclass of {}'.format(first, second)
      raise self._type(self._message(msg, custom))


  def is_not_subclass(self, first, second, custom=None):
    if not is_class(first):
      raise TypeError('First value must be a class')

    if not class_or_tuple(second):
      raise TypeError('Second value must be a class or tuple of classes')

    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if issubclass(first, second):
      first = class_names(first)
      second = class_names(second)
      msg = '{} is a subclass of {}'.format(first, second)
      raise self._type(self._message(msg, custom))


  def is_instance(self, first, second, custom=None):
    if not class_or_tuple(second):
      raise TypeError('Second value must be a class or tuple of classes')

    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not isinstance(first, second):
      second = class_names(second)
      msg = '{} is not an instance of {}'.format(first, second)
      raise self._type(self._message(msg, custom))

  isa = is_instance


  def is_not_instance(self, first, second, custom=None):
    if not class_or_tuple(second):
      raise TypeError('Second value must be a class or tuple of classes')

    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if isinstance(first, second):
      second = class_names(second)
      msg = '{} is an instance of {}'.format(first, second)
      raise self._type(self._message(msg, custom))

  is_not_a = is_not_instance


  def keys(self, obj, required=None, extra=None, optional=None, custom=None):
    if not isinstance(obj, (dict,)):
      raise TypeError('First value must be a dict')

    required = [] if required is None else required
    optional = [] if optional is None else optional

    if extra is None and len(optional) == 0:
      extra = True
    elif extra is None and len(optional) > 0:
      extra = False

    if not string_list(required):
      raise TypeError('Required key list must be a list of strings')

    if not string_list(optional):
      raise TypeError('Optional key list must be a list of strings')

    if not isinstance(extra, bool):
      raise TypeError('Value for extra must be a boolean')

    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    key_list = obj.keys()

    missing_keys = []
    for key in required:
      if key in key_list:
        key_list.remove(key)
      else:
        missing_keys.append(key)

    if not extra:
      for key in optional:
        if key in key_list:
          key_list.remove(key)

      if len(key_list) > 0 and len(missing_keys) > 0:
        msg = 'Dict is missing keys {} and has extra keys {}'.format(missing_keys, key_list)
        raise self._type(self._message(msg, custom))
      elif len(key_list) > 0:
        msg = 'Dict has extra keys {}'.format(key_list)
        raise self._type(self._message(msg, custom))

    if len(missing_keys) > 0:
      msg = 'Dict is missing keys {}'.format(missing_keys)
      raise self._type(self._message(msg, custom))


  def that(self, value):
    return InsistThat(value, self._type, self._prefix, self._both)


class InsistThat(Insist):
  def __repr__(self):
    return '< successful insist that chain >'


  def __init__(self, value, error_type, message_prefix, always_show_standard):
    self.__value = value

    super(InsistThat, self).__init__(error_type, message_prefix, always_show_standard)


  def true(self, custom=None):
    super(InsistThat, self).true(self.__value, custom)

    return self


  def false(self, custom=None):
    super(InsistThat, self).false(self.__value, custom)

    return self


  def equal(self, second, custom=None):
    super(InsistThat, self).equal(self.__value, second, custom)

    return self

  equals = equal


  def not_equal(self, second, custom=None):
    super(InsistThat, self).not_equal(self.__value, second, custom)

    return self

  not_equals = not_equal


  def less(self, second, custom=None):
    super(InsistThat, self).less(self.__value, second, custom)

    return self


  def less_equal(self, second, custom=None):
    super(InsistThat, self).less_equal(self.__value, second, custom)

    return self


  def greater(self, second, custom=None):
    super(InsistThat, self).greater(self.__value, second, custom)

    return self


  def greater_equal(self, second, custom=None):
    super(InsistThat, self).greater_equal(self.__value, second, custom)

    return self


  def is_same(self, second, custom=None):
    super(InsistThat, self).is_same(self.__value, second, custom)

    return self


  def is_not(self, second, custom=None):
    super(InsistThat, self).is_not(self.__value, second, custom)

    return self


  def is_in(self, second, custom=None):
    super(InsistThat, self).is_in(second, self.__value, custom)

    return self


  def not_in(self, second, custom=None):
    super(InsistThat, self).not_in(second, self.__value, custom)

    return self


  def has(self, first, custom=None):
    second = self.__value

    if not is_iterable(second):
      raise TypeError('Value must be an iterable object')

    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not (first in second):
      msg = '{} in {} fails'.format(first, second)
      raise self._type(self._message(msg, custom))

    return self


  def not_has(self, first, custom=None):
    second = self.__value

    if not is_iterable(second):
      raise TypeError('Value must be an iterable object')

    if not string_or_none(custom):
      raise TypeError('Custom message must be a string or None')

    if not (first not in second):
      msg = '{} not in {} fails'.format(first, second)
      raise self._type(self._message(msg, custom))

    return self


  def is_subclass(self, second, custom=None):
    super(InsistThat, self).is_subclass(self.__value, second, custom)

    return self


  def is_not_subclass(self, second, custom=None):
    super(InsistThat, self).is_not_subclass(self.__value, second, custom)

    return self


  def is_instance(self, second, custom=None):
    super(InsistThat, self).is_instance(self.__value, second, custom)

    return self

  isa = is_instance


  def is_not_instance(self, second, custom=None):
    super(InsistThat, self).is_not_instance(self.__value, second, custom)

    return self

  is_not_a = is_not_instance


  def keys(self, required=None, optional=None, extra=True, custom=None):
    super(InsistThat, self).keys(self.__value, required, optional, extra, custom)

    return self


  def that(self, value):
    raise RuntimeError('Cannot call method "that" more than once in an insist chain')
