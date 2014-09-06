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

import inspect, collections

try:
  string_types = (str, unicode)
except NameError:
  string_types = (str, )

none_type = (type(None), )


def is_iterable(obj):
  return isinstance(obj, collections.Iterable)

def is_class(obj):
  return inspect.isclass(obj)


def exception_class(obj):
  if not is_class(obj):
    return False

  return issubclass(obj, Exception)


def string_or_none(obj):
  return isinstance(obj, string_types + none_type)


def class_or_tuple(obj):
  if is_class(obj):
    return True

  if not isinstance(obj, tuple):
    return False

  for item in obj:
    if not is_class(item):
      return False

  return True


def class_names(obj):
  if is_class(obj):
    return obj.__name__

  if not isinstance(obj, tuple):
    raise TypeError('Value must be a class or tuple of classes')

  result = []

  for item in obj:
    if not is_class(item):
      raise TypeError('Value must be a class or tuple of classes')

    result.append(item.__name__)

  return tuple(result)

def string_list(obj):
  if not isinstance(obj, (list, set, tuple)):
    return False

  for item in obj:
    if not isinstance(item, string_types):
      return False

  return True
