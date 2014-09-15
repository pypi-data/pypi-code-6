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

from PyQt5 import QtWidgets, QtGui, QtCore


from trv._model import TestModel
from trv._view import TestWidget

import testtools
from subunit.v2 import ByteStreamToStreamResult


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.test_tree_view = TestWidget(self)
        self.setCentralWidget(self.test_tree_view)
        self.test_tree_model = TestModel()
        self.test_tree_view.setModel(self.test_tree_model)
        self.create_toolbar_and_menus()
        self.readSettings()

    def create_toolbar_and_menus(self):
        toolbar = self.addToolBar("Actions")
        fileMenu = self.menuBar().addMenu("&File")

        def add_to_toolbar_and_menu(menu, *args):
            nonlocal toolbar
            nonlocal fileMenu
            action = toolbar.addAction(*args)
            menu.addAction(action)
            return action

        open_file_action = add_to_toolbar_and_menu(
            fileMenu,
            QtGui.QIcon.fromTheme("gtk-open"),
            "Open From File",
        )
        open_file_action.triggered.connect(self.on_open_file)
        open_url_action = add_to_toolbar_and_menu(
            fileMenu,
            QtGui.QIcon.fromTheme("network"),
            "Open From URL"
        )
        open_url_action.triggered.connect(self.on_open_url)
        open_url_action.setEnabled(False)
        exit_action = fileMenu.addAction("Exit")
        exit_action.triggered.connect(self.close)

    def on_open_file(self):
        s2d = testtools.StreamToDict(self.test_tree_model.add_test)
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open Subunit Stream",
        )
        if file_path:
            with open(file_path, 'rb') as subunit_file:
                self.test_tree_model.reset()
                s2d.startTestRun()
                reader = ByteStreamToStreamResult(
                    subunit_file,
                    'autopilot_stdout'
                )
                reader.run(s2d)
                s2d.stopTestRun()

    def on_open_url(self):
        pass

    def readSettings(self):
        settings = QtCore.QSettings()
        geometry = settings.value("geometry")
        if geometry is not None:
            self.restoreGeometry(geometry.data())
        else:
            self.setGeometry(0, 0, 1204, 768)
        window_state = settings.value("windowState")
        if window_state is not None:
            self.restoreState(window_state.data())
        splitter_state = settings.value("splitter_state")
        if splitter_state is not None:
            self.test_tree_view.restoreState(splitter_state)

    def closeEvent(self, event):
        settings = QtCore.QSettings()
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        settings.setValue("splitter_state", self.test_tree_view.saveState())
