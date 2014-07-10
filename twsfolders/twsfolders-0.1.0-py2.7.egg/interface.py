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

from zope.interface import Interface, Attribute


class IItem(Interface):

    id = Attribute('')
    sid = Attribute('')
    name = Attribute('')
    title = Attribute('')
    description = Attribute('')
    parent = Attribute('')
    folder = Attribute('')
    created = Attribute('')
    modified = Attribute('')

    def has_property(self, name):
        """

        :param name:
        :return:
        """

    def get_property(self, name, default=None):
        """

        :param name:
        :param default:
        :return:
        """

    def set_property(self, name, value):
        """

        :param name:
        :param value:
        :return:
        """

    def get_properties(self, view=None):
        """

        :param view:
        :return:
        """

    def set_properties(self, properties):
        """

        :param properties:
        :return:
        """

    def mark_changed(self):
        """

        :return:
        """

    def get_url_item(self, url):
        """

        :param url:
        :return:
        """


class IFolder(IItem):

    def add_item(self, item, overwrite=False):
        """

        :param item:
        :param overwrite:
        :return:
        """

    def has_item(self, name):
        """

        :param name:
        :return:
        """

    def get_item(self, name):
        """

        :param name:
        :return:
        """

    def rename_item(self, name, new_name, overwrite=False):
        """

        :param name:
        :param new_name:
        :param overwrite:
        :return:
        """

    def delete_item(self, name):
        """

        :param name:
        :return:
        """

    def delete_items(self, names):
        """

        :param names:
        :return:
        """

    def move_item(self, name, target_folder, overwrite=False):
        """

        @param name:
        :param target_folder:
        :param overwrite:
        :return:
        """

    def list_items(self, **kwargs):
        """

        :param kwargs:
        :return:
        """

    def len_items(self):
        """

        :return:
        """


class IRootFolders(Interface):
    pass
