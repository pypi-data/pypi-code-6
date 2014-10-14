#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Pydouble deletes duplicate files in a directory and
    delete some files by extension.

    Duplicate files are moved to the directory selected duplicates.

"""

__title__ = 'Pydouble'
__version__ = '1.4.1'
__author__ = 'julien@hautefeuille.eu'

import os
import sys

from PySide.QtCore import QObject, QThread, Signal
from PySide.QtGui import QMainWindow, QApplication
from PySide.QtGui import QFileDialog

from job import Duplicate

from UI import Ui_MainWindow

os.environ["QT_API"] = "pyside"


class CustomSignal(QObject):
    """
        This signal is used to store the data sent when processing
        files and distribute them in the appropriate text fields.

    """
    datasig = Signal(dict)


class MainThread(QThread):
    """
        Thread file processing

    """
    def __init__(self, parent=None):
        """
            Paths are initialized to access, the list containing the
            extensions, we initialize the variable responsible for monitoring
            the processing task and then creates an instance of the
            custom signal.

        """
        super(MainThread, self).__init__(parent)
        self.spath = ""
        self.dpath = ""
        self.exten = ""
        self.thash = ""
        self.exiting = False
        self.signal = CustomSignal()

    def run(self):
        """
            This function is responsible for running the main treatment on
            files. It is the processing thread.
            This function successively tests the files to delete, mark
            duplicates and sends the processed data to the interface
            through personalized transmitted signal.

        """
        while self.exiting is False:
            dupli = Duplicate(source=self.spath,
                              destination=self.dpath,
                              extension=self.exten,
                              typehash=self.thash)
            for line in dupli.run():  # Le générateur
                self.signal.datasig.emit(line)
            self.exiting = True  # Quand le travail est terminé, on sort.


class MainWindow(QMainWindow, Ui_MainWindow):
    """
        Class responsible for controlling the user interface.

    """
    def __init__(self, parent=None):
        """
            This initialization function initializes the window
            graph, instantiate the main thread processing and
            connect the signals to different slots.

        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.mainthread = MainThread()
        self.mainthread.signal.datasig.connect(self.update_window)
        self.mainthread.started.connect(self.started_process)
        self.mainthread.finished.connect(self.finished_process)
        self.mainthread.terminated.connect(self.terminated_process)

        self.runButton.clicked.connect(self.start_process)
        self.sourceButton.clicked.connect(self.open_file_dialog)
        self.doublonButton.clicked.connect(self.open_file_dialog)
        self.removeEdit.editingFinished.connect(self.init_extension)

    def start_process(self):
        """
            We check if the thread is started, if not, we will start.

        """
        if not self.mainthread.isRunning():
            self.mainthread.exiting = False
            if self.radioSHA1.isChecked():
                self.mainthread.thash = "sha1"
            elif self.radioMD5.isChecked():
                self.mainthread.thash = "md5"
            else:
                self.mainthread.thash = "sha1"
            self.mainthread.start()

    def stop_process(self):
        """
            We check if the thread is started, if so, it quits.

        """
        if self.mainthread.isRunning():
            self.mainthread.exiting = True

    def started_process(self):
        """
            Initialization when the thread starts.

        """
        [e.setEnabled(False) for e in [self.sourceButton,
                                       self.doublonButton,
                                       self.removeEdit,
                                       self.radioMD5,
                                       self.radioSHA1]]
        [e.clear() for e in [self.fTextEdit, self.dTextEdit, self.rTextEdit]]
        self.lcdCounter.display(0)
        self.runButton.setEnabled(False)
        self.fTextEdit.appendPlainText('Job started')
        self.fTextEdit.appendPlainText('Wait...')

    def finished_process(self):
        """
            When the thread is finished.

        """
        [e.setEnabled(True) for e in [self.sourceButton,
                                      self.doublonButton,
                                      self.removeEdit,
                                      self.radioMD5,
                                      self.radioSHA1,
                                      self.runButton]]
        self.fTextEdit.appendPlainText('Job stopped')

    def terminated_process(self):
        """
            When the thread is finished. Is not raised in the case.

        """
        self.fTextEdit.appendPlainText('Job terminated')

    def update_window(self, data):
        """
            Updating the user interface. Distribution of messages.

        """
        self.lcdCounter.display(data["coun"])
        msg = ("%s \t %s" % (data["hash"], data["file"]))
        if "dupl" in data.iterkeys():
            self.dTextEdit.appendPlainText(msg)
        elif "kill" in data.iterkeys():
            self.rTextEdit.appendPlainText(msg)
        else:
            self.fTextEdit.appendPlainText(msg)

    def init_extension(self):
        """
            File extensions was treated and updates the list
            extensions for initialization processing thread.

        """
        self.mainthread.exten = self.removeEdit.text()

    def open_file_dialog(self):
        """
            Function manages the selection of files, you can recover the sender
            signal to change the state of the button.

        """
        flags = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(
            self, "Open Directory", os.getcwd(), flags)
        if self.sender() is self.sourceButton:
            self.sender().setText(directory)
            self.mainthread.spath = directory
        if self.sender() is self.doublonButton:
            self.sender().setText(directory)
            self.mainthread.dpath = directory


def main():
    """
        Main launch function of the program, an application instantiate
        Qt and our graphics renderer class user interface.

    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
