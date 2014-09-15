#
# trv: A graphical test result viewer
# Copyright (C) 2014 Canonical
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Model code for TRV."""

from PyQt5 import QtCore, QtGui


class TestModel(QtCore.QAbstractListModel):

    """A model class for a test result.

    This class exposes a Qt tree model API, and stores test results internally.

    """

    def __init__(self):
        super().__init__()
        self._tests = []

    def add_test(self, test_details):
        new_pos = len(self._tests)
        self.beginInsertRows(QtCore.QModelIndex(), new_pos, new_pos)
        self._tests.append(test_details)
        self.endInsertRows()

    def reset(self):
        self.beginResetModel()
        self._tests = []
        self.endResetModel()

    # Methods required for Qt5 model classes:
    def rowCount(self, index):
        # return number of rows under 'index', which may be invalid, in which
        # case, return the number of rows at the root level.
        rows = 0
        if not index.isValid():
            rows = len(self._tests)
        return rows

    def data(self, index, role):
        # Returns the data stored under the given role for the item referred to by the index.
        # Note: If you do not have a value to return, return an invalid QVariant instead of returning 0.
        if 0 <= index.row() < len(self._tests) and index.column() == 0:
            if role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(self._tests[index.row()]['id'])
            if role == QtCore.Qt.SizeHintRole:
                return QtCore.QSize(400, 20)
            if role == QtCore.Qt.DecorationRole:
                return get_icon_for_status(
                    self._tests[index.row()]['status']
                ).pixmap(QtCore.QSize(12, 12))

        return QtCore.QVariant()

    def get_test_dict_for_index(self, index):
        """Get the test dictionary for a given model index."""
        if (
            index.isValid()
            and 0 <= index.row() < len(self._tests)
            and index.column() == 0
        ):
            return self._tests[index.row()]
        return dict()


def get_icon_for_status(status):
    if status in ('success', 'xfail', 'exists'):
        return QtGui.QIcon(":icons/green")
    elif status == 'skip':
        return QtGui.QIcon(":icons/yellow")
    elif status in ('fail', 'uxsuccess'):
        return QtGui.QIcon(":icons/red")
    else:
        return QtGui.QIcon(":icons/grey")
