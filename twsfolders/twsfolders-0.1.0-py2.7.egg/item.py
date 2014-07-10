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

import datetime
import uuid

from zope.interface import implementer
from persistent import Persistent
from persistent.mapping import PersistentMapping

from _compat import is_string, is_integer
from _logger import log_debug

from interface import IItem
import folder
import prefixes

URL_SEPARATOR = prefixes.URL_SEPARATOR


class ErrorDetachParent(Exception):
    """ Want to detach Parent folder when Item is still in it's collection"""


class ErrorAttachParent(Exception):
    """ Want to attach Parent folder when Item is not in it's collection"""


class NotRenameAbleError(Exception):
    """Item rename not allowed"""


@implementer(IItem)
class Item(Persistent):

    def __init__(self, parent=None, name=None, title=None, description=None, overwrite=False, **kwargs):

        self.__parent = None
        self.__sid = self.get_new_sid()
        self.__name = None
        self.__title = None
        self.__description = None
        self.__dateTimeCreated = datetime.datetime.now()
        self.__dateTimeModified = datetime.datetime.now()

        self.name = name
        self.title = title
        self.description = description
        self.__properties = PersistentMapping()

        if parent:
            parent.add_item(self, overwrite=overwrite)

    def __repr__(self):
        class_ = self.__class__
        return repr('<%s.%s object at %#x with id:"%s: url:"%s">' % (class_.__module__, class_.__name__,
                                                                     id(self), self.id, self.url()
                                                                     )
                    )

    def mark_changed(self):
        self.__dateTimeModified = datetime.datetime.now()
        self._p_changed = 1

    @property
    def rename_able(self):
        """
        Check if I can be renamed, an item can be renamed only if it is not plugged to a folder
        @return True or False
        """

        if self.__parent is None:
            return True

        return False

    @property
    def name(self):
        return self.__name

    def validate_name(self, name):
        if not name or not self.is_string(name) or URL_SEPARATOR in name:
            return False

        return True

    @name.setter
    def name(self, name):
        # i will set my name only if me parent is None
        if self.rename_able:
            if self.validate_name(name):
                self.__name = name
            else:
                raise TypeError('item name not valid')
        else:
            raise NotRenameAbleError('i am in a folder, use folder.rename_item')

    # by default synonym of name
    def get_id_name(self):
        return 'name'

    def get_id(self):
        return getattr(self, self.get_id_name(), None)

    @property
    def id_name(self):
        return self.get_id_name()

    @property
    def id(self):
        return self.get_id()

    @property
    def sid(self):
        return self.__sid

    @property
    def title(self):
        if self.__title is None:
            return self.name
        else:
            return self.__title

    @title.setter
    def title(self, value):
        if (value and self.is_string(value)) or value is None:
            self.__title = value
        else:
            raise TypeError('title must string or None received %s' % type(value))

    @property
    def description(self):
        if self.__description is None:
            return self.title
        else:
            return self.__description

    @description.setter
    def description(self, value):
        if (value and self.is_string(value)) or value is None:
            self.__description = value
        else:
            raise TypeError('description must string or None received %s' % type(value))

    @property
    def created(self):
        return str(self.__dateTimeCreated)

    @property
    def modified(self):
        return str(self.__dateTimeModified)

    @property
    def root(self):
        if self.is_folder and self.parent is None:
            return True

        return False

    @property
    def is_folder(self):
        return False

    @property
    def parent(self):
        return self.__parent

    def inform_parent_attached(self, parent):
        """
        this is a private package function
        This function is called from folder containing this item
        to inform that it has been added to it's children collection
        @param parent: Folder
        @return: boolean
        """

        # I'll be attached to a parent folder only if i have no parent
        # and i must be already in the parent folder children collection
        if self.parent is None and parent.is_folder and self.name in parent:
            self.__parent = parent
            self.mark_changed()
            return True

        return False

    def inform_parent_detached(self):
        """
        this is a private package function
        This function is called from folder containing this item
        to inform that it has been removed from it's children collection
        @return: boolean
        """

        # i will detach my self from my parent only if i am no longer in my parent
        if self.parent is not None and self.name not in self.parent:
            self.__parent = None
            self.mark_changed()
            return True

        return False

    def allow_delete(self):
        """
        Check if I can be deleted
        @return True or False
        """

        return True

    def allow_move(self, target_folder):
        """
        Check if I am allowed to move to target folder
        @param target_folder: Folder
        @return True or False
        """

        return True

    def get_parents(self, validator=None):
        """
        :param validator interface or callable
        :return: list of parent until root reached or if validator is submitted, until parent validate
        """
        parents = []
        folder_parent = self.parent

        while folder_parent:
            parents.append(folder_parent)
            if validator:
                if (prefixes.is_interface(validator) and validator.providedBy(folder_parent)) or \
                        (not prefixes.is_interface(validator) and callable(validator) and validator(folder_parent)):

                    break

            folder_parent = folder_parent.parent

        return parents

    def is_folder_in_parents(self, folder_item):
        """
        Check whether i am in the hierarchy tree of folder
        for example /a/folder/v/c/item
        @param folder_item: Folder
        @return: boolean
        """
        if not isinstance(folder_item, folder.Folder):
            return False

        # go through my parents and try to find folder
        folder_parent = self.parent
        # go through the hierarchy of my parents and try to find folder
        while folder_parent:
            if folder_item == folder_parent:
                return True

            folder_parent = folder_parent.parent

        return False

    # properties operations
    def __getitem__(self, key):
        return self.get_property(key)

    def __delitem__(self, key):
        if key in self.__properties.keys():
            del self.__properties[key]
            self.mark_changed()

    def __setitem__(self, key, value):
        self.set_property(key, value)

    def has_property(self, name):
        return name in self.__properties

    def get_property(self, name, default=None):

        if name in ('name', 'id', 'title', 'description', 'created', 'modified'):
            return getattr(self, name)

        if name in self.__properties:
            return self.__properties[name]

        return default

    def set_property(self, name, value):
        if self.is_string(name, raise_err=True):
            self.__properties[name] = value
            self.mark_changed()

    def get_properties(self, properties):
        if not properties:
            return []

        if not isinstance(properties, (list, tuple)):
            raise TypeError('properties must be list or tuple received: %s' % type(properties))

        view = {}
        for key in properties:
            view[key] = self.get_property(key)

        return view

    def set_properties(self, properties):
        if properties is None:
            properties = dict()

        if not isinstance(properties, dict):
            raise TypeError('expected dict type, received %s' % type(properties))

        for name, value in properties.items():
            self.set_property(name, value)

        return True

    def get_url_item(self, url):
        """
        :param url: str, of type
        """

        if not url:
            url = URL_SEPARATOR

        if self.is_string(url, raise_err=True):
            #log_debug('get_url_item - url: %s' % url)
            sep_url = url.split(URL_SEPARATOR)
            ind = 0
            item = self
            len_sep_url = len(sep_url)
            for tu in sep_url:
                if tu == '' and ind == 0:
                    # if the first one is empty, this is the url separator
                    tu = URL_SEPARATOR

                elif tu == '':
                    # ignore empty ones
                    ind += 1
                    continue

                if prefixes.has_prefix(tu):
                    # I would like to pass the next item to some validators that can need it
                    #next_item_name
                    if ind < len_sep_url-1:
                        next_item_name = sep_url[ind+1]
                    else:
                        next_item_name = None

                    item = prefixes.get_parent(tu, item, next_item_name=next_item_name)
                    #log_debug('... get parent from prefix "%s"' % tu)

                    if item is None:
                        #log_debug('... parent from prefix "%s" not found' % tu)
                        break

                    ind += 1
                    continue

                if not item.is_folder:
                    item = None
                    break

                item = item.get_item(tu)
                if item is None:
                    break

                ind += 1

            if item is None:
                #@log_debug('... url do not exist: %s' % url)
                pass

            #log_debug('... return %s' % item)
            return item

    def url(self, prefix=None):
        """
        @param prefix: str the prefix registered in module prefixes, by default prefix='/'
        @return: string , the url of this item from the prefix parent '/' is the root
        """

        if not prefix:
            prefix = URL_SEPARATOR

        # will go through parents until i found a parent that is validated by this prefix
        #log_debug('url - item: %s, prefix: "%s"' % (self, prefix))
        url_list = []
        item = self
        found = False
        while item:
            if prefixes.validate_item_by_prefix(prefix, item, item_caller=self):
                url_list.append(prefix)
                found = True
                break

            url_list.append(item.name)
            item = item.parent

        if found:
            url_list.reverse()
            if url_list and url_list[0] == URL_SEPARATOR:
                url_list[0] = ''

            if len(url_list) == 1 and url_list[0] == '':
                #this is the root item
                url_text = URL_SEPARATOR
            else:
                url_text = URL_SEPARATOR.join(url_list)

        else:
            #log_debug('...getting url of item with prefix "%s" not found' % prefix)
            url_text = ''

        #log_debug('... return: %s' % url_text)
        return url_text

    @staticmethod
    def get_new_sid():
        return uuid.uuid4().hex

    @staticmethod
    def is_string(value, raise_err=False):
        if is_string(value):
            return True
        else:
            if raise_err:
                raise TypeError('expected string type, received %s' % type(value))

            return False

    @staticmethod
    def is_integer(value, raise_err=False):
        if is_integer(value):
            return True
        else:
            if raise_err:
                raise TypeError('expected integer type, received %s' % type(value))

            return False
