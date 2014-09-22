# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dvi_viewer.ui'
#
# Created: Thu Sep  4 13:41:06 2014
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName(_fromUtf8("main_window"))
        main_window.resize(800, 600)
        self.central_widget = QtGui.QWidget(main_window)
        self.central_widget.setObjectName(_fromUtf8("central_widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.central_widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.dvi_graphics_view = QtGui.QGraphicsView(self.central_widget)
        self.dvi_graphics_view.setObjectName(_fromUtf8("dvi_graphics_view"))
        self.verticalLayout.addWidget(self.dvi_graphics_view)
        main_window.setCentralWidget(self.central_widget)
        self.menubar = QtGui.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(main_window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        main_window.setStatusBar(self.statusbar)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(_translate("main_window", "MainWindow", None))

