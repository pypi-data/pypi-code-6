"""
Copyright (C) 2014 Haak Saxberg

This file is part of Solid, a state machine package for Python.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""


class ReadOnlyStateWrapper(object):

    def __init__(self, instance):
        self._instance = instance

    def __setattr__(self, name, value):
        if name == "_instance":
            super(ReadOnlyStateWrapper, self).__setattr__(name, value)
        else:
            raise AttributeError(
                u"Can't set attribute -- ReadOnlyWrapped object.",
            )

    def __getattr__(self, name):
        return getattr(self._instance, name)

    def __repr__(self):
        return u"<ReadOnly:{}>".format(self._instance)

    def __eq__(self, other):
        if not isinstance(other, ReadOnlyStateWrapper):
            return NotImplemented

        return self._instance == other._instance
