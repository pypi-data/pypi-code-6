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

""" View classes for TRV."""
import locale
import enum
from PyQt5 import QtWidgets, QtCore, QtGui


class TestWidget(QtWidgets.QSplitter):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setChildrenCollapsible(False)

        # create the user interface components:
        self.test_id_view = QtWidgets.QListView(self)
        self.test_id_view.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.test_id_view.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.test_detail_view = TestView(self)
        self.test_id_view.clicked.connect(self._on_test_changed)
        self.setStretchFactor(0, 0)
        self.setStretchFactor(1, 1)

    def setModel(self, model):
        self.test_id_view.setModel(model)
        # import pudb; pudb.set_trace()

    def _on_test_changed(self, model_index):
        test_details = model_index.model().get_test_dict_for_index(model_index)
        self.test_detail_view.set_test_dict(test_details)


class TestView(QtWidgets.QWidget):

    """A class that renders details from a test."""

    def __init__(self, parent):
        super().__init__(parent)
        vert_layout = QtWidgets.QVBoxLayout(self)

        # Add the grid layout items:
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(
            QtWidgets.QLabel("Test Id:", self),
            0,
            0,
        )
        self.test_id = QtWidgets.QLabel(self)
        grid_layout.addWidget(self.test_id, 0, 1)

        grid_layout.addWidget(
            QtWidgets.QLabel("Status:", self),
            1,
            0,
        )
        self.test_status = QtWidgets.QLabel(self)
        grid_layout.addWidget(self.test_status, 1, 1)
        grid_layout.setColumnStretch(1, 100)
        vert_layout.addLayout(grid_layout)

        self.details_container = DetailsContainer()
        vert_layout.addWidget(self.details_container, 100)
        vert_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

    def set_test_dict(self, test_dict):
        self.test_id.setText("")
        self.test_status.setText("")
        self.details_container.reset()

        if test_dict:
            self.test_id.setText(test_dict['id'])
            self.test_status.setText(test_dict['status'])
            sorted_detail_keys = sorted(
                test_dict['details'].keys(),
                key=locale.strxfrm
            )
            for k in sorted_detail_keys:
                v = test_dict['details'][k]
                self.details_container.add_content_widget(
                    ContentWidget.create_for_mime_type(v.content_type)(k, v)
                )
            self.setEnabled(True)


class DetailsContainer(QtWidgets.QToolBox):

    def __init__(self):
        super().__init__()
        self._details = []

    def reset(self):
        while self.count():
            self.removeItem(0)
        self._details = []

    def add_content_widget(self, widget):
        self.addItem(widget, widget.content_name)
        self._details.append(widget)


class ContentWidget(QtWidgets.QFrame):

    """This is a base class for all content viewer objects.

    It implements an expanding viewer for the detail object. The viewer can be
    in one of two states: 'summary' or 'expanded'.

    In summary mode, we display the summary text and a link to expand the
    widget.

    In expanded mode, we display the full data of the content object.

    """

    class State(enum.Enum):

        Collapsed = 0
        Expanded = 1

    def __init__(self, content_name, content_object, parent=None):
        super().__init__(parent)
        # self.setFrameStyle(QtWidgets.QFrame.StyledPanel)
        self._content_object = content_object
        self.content_name = "%s (%s)" % (
            content_name,
            "/".join((
                content_object.content_type.type,
                content_object.content_type.subtype,
            ))
        )
        self.detail_widget = self._create_display_widget(content_object)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.detail_widget, 0, 0)

    def _create_display_widget(self, content_object):
        """Create a display widget for 'content_object' and return it."""
        # subclasses should re-implement this and do something more sensible.
        return QtWidgets.QLabel(
            "Unrepresentable content object of type: "
            + str(content_object.content_type)
        )

    @staticmethod
    def create_for_mime_type(mime_type):
        if mime_type.type == 'text':
            return TextContentWidget
        elif mime_type.type == 'image':
            return ImageContentWidget
        return ContentWidget


class TextContentWidget(ContentWidget):

    def _create_display_widget(self, content_object):
        edit = QtWidgets.QPlainTextEdit()
        edit.setPlainText(content_object.as_text())
        edit.setReadOnly(True)
        edit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        return edit


class ImageContentWidget(ContentWidget):

    class ImageViewScrollArea(QtWidgets.QScrollArea):

        def __init__(self, image_data):
            super().__init__()
            self.label = QtWidgets.QLabel(self)
            pixmap = QtGui.QPixmap()
            if not pixmap.loadFromData(image_data):
                self.label.setText("Could not load image :(")
            else:
                self.label.setPixmap(pixmap)
                self.label.setBackgroundRole(QtGui.QPalette.Base)
                self.label.setSizePolicy(
                    QtWidgets.QSizePolicy.Ignored,
                    QtWidgets.QSizePolicy.Ignored
                )
                self.label.setScaledContents(True)
                self.setBackgroundRole(QtGui.QPalette.Dark)
                self.setWidget(self.label)
                self.setSizePolicy(
                    QtWidgets.QSizePolicy.Expanding,
                    QtWidgets.QSizePolicy.Expanding,
                )

        def resizeEvent(self, event):
            pixmap_size = self.label.pixmap().size()
            viewport_size = event.size()
            pixmap_size.scale(viewport_size, QtCore.Qt.KeepAspectRatio)
            self.label.resize(pixmap_size)
            return super().resizeEvent(event)

    def _create_display_widget(self, content_object):
        img_data = QtCore.QByteArray(b''.join(content_object.iter_bytes()))
        return ImageContentWidget.ImageViewScrollArea(img_data)
