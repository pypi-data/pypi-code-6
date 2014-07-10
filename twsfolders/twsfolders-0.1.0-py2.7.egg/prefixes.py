# Copyright 2013 Djebran Lezzoum All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from zope.interface.interface import InterfaceClass

from interface import IItem
import _compat

from _logger import log_debug

URL_SEPARATOR = '/'

_registry = {}


def is_interface(validator):
    return isinstance(validator, InterfaceClass)


class _Prefix(object):

    def __init__(self, name, validator, getter):
        self.name = name
        self.validator = validator
        self.getter = getter

    @staticmethod
    def get_parent_by_validator(item, validator, **kwargs):
        log_debug('get parent from item: %s by validator:  %s ' % (item, validator), 'get_parent_by_validator')
        if not IItem.providedBy(item):
            raise Exception('item do provide IItem')

        parent_item = item

        while parent_item:
            log_debug(' ... look parent_item: %s ' % parent_item, 'get_parent_by_validator')
            #if (is_interface(validator) and validator.providedBy(parent_item)) or \
            #        (not is_interface(validator) and callable(validator) and validator(parent_item, **kwargs)):
            if validate_item(parent_item, validator, **kwargs):
                log_debug(' ... parent_item validated by interface: %s' % parent_item, 'get_parent_by_validator')
                break

            parent_item = parent_item.parent

        log_debug('return: %s' % parent_item, 'get_parent_by_validator')
        return parent_item

    def get_parent(self, item, **kwargs):
        if self.getter:
            return self.getter(item, **kwargs)

        elif self.validator:
            return self.get_parent_by_validator(item, self.validator, **kwargs)

    def validate(self, item, **kwargs):
        if self.validator:
            if is_interface(self.validator):
                # validator is a zope interface
                return self.validator.providedBy(item)

            else:
                # validator can be only callable
                return self.validator(item, **kwargs)

        return False


def register(prefix_name, validator=None, getter=None):

    global _registry

    if not isinstance(prefix_name, _compat.string_types):
        raise TypeError('prefix name must be a string')

    # validator can be None
    if validator is not None and not is_interface(validator) and not callable(validator):
        raise TypeError('validator must be interface or callable')

    # getter can not be None if validator is None
    if not validator and not callable(getter):
        raise TypeError('getter must be callable, if no validator ')

    _registry[prefix_name] = _Prefix(prefix_name, validator, getter)


def get_parent(prefix, item, **kwargs):
    global _registry

    pr = _registry.get(prefix, None)
    if pr:
        return pr.get_parent(item, **kwargs)

    return None


def validate_item(item, validator, **kwargs):
    if (is_interface(validator) and validator.providedBy(item)) or \
            (not is_interface(validator) and callable(validator) and validator(item, **kwargs)):
        return True

    return False


def validate_item_by_prefix(prefix, item, **kwargs):
    global _registry
    pr = _registry.get(prefix, None)
    if pr:
        return pr.validate(item, **kwargs)

    return False


def has_prefix(prefix):
    global _registry
    if prefix in _registry:
        return True

    return False


def root_folder_validator(item, **kwargs):

    if item.parent is None:
        # can assert if the root of item_caller with parent_folder_getter
        return True

    return False


def parent_folder_getter(item, **kwargs):
    """
    :param item: C{Item} , storage item or folder
    :return: C{Folder} the parent of item
    """
    return item.parent


def private_folder_getter(item, **kwargs):
    return item.private_folder


def sibling_parent_getter(item, **kwargs):
    """ return the the first item that contain next_item_name"""
    next_item_name = kwargs.get('next_item_name', None)
    if next_item_name is None:
        return None

    parent_item = item.parent

    while parent_item:

        if next_item_name in parent_item:
            return parent_item

        parent_item = parent_item.parent

    #not found
    return None


def _init():
    register(URL_SEPARATOR, validator=root_folder_validator)
    register('..', getter=parent_folder_getter)
    register('~', getter=sibling_parent_getter)
    register('@', getter=private_folder_getter)


_init()
