# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtarmsim/ui/consola.ui'
#
# Created: Tue Sep  2 17:00:02 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_Consola(object):
    def setupUi(self, Consola):
        Consola.setObjectName(_fromUtf8("Consola"))
        Consola.resize(295, 302)
        Consola.setWindowTitle(_fromUtf8(""))
        self.centralWidget = QtGui.QWidget(Consola)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        Consola.setCentralWidget(self.centralWidget)

        self.retranslateUi(Consola)
        QtCore.QMetaObject.connectSlotsByName(Consola)

    def retranslateUi(self, Consola):
        pass

from ..res import oxygen_rc
