# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtarmsim/ui/breakpo.ui'
#
# Created: Tue Sep  2 17:00:03 2014
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

class Ui_Break(object):
    def setupUi(self, Break):
        Break.setObjectName(_fromUtf8("Break"))
        Break.resize(400, 300)

        self.retranslateUi(Break)
        QtCore.QMetaObject.connectSlotsByName(Break)

    def retranslateUi(self, Break):
        Break.setWindowTitle(_translate("Break", "Puntos de ruptura", None))

from ..res import oxygen_rc
