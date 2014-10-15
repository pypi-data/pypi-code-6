# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtarmsim/ui/multi.ui'
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

class Ui_Multipasos(object):
    def setupUi(self, Multipasos):
        Multipasos.setObjectName(_fromUtf8("Multipasos"))
        Multipasos.resize(400, 101)
        self.pasoslabel = QtGui.QLabel(Multipasos)
        self.pasoslabel.setGeometry(QtCore.QRect(20, 30, 87, 16))
        self.pasoslabel.setObjectName(_fromUtf8("pasoslabel"))
        self.pasos = QtGui.QLineEdit(Multipasos)
        self.pasos.setGeometry(QtCore.QRect(20, 50, 113, 20))
        self.pasos.setObjectName(_fromUtf8("pasos"))
        self.aceptarButton = QtGui.QPushButton(Multipasos)
        self.aceptarButton.setGeometry(QtCore.QRect(280, 20, 75, 23))
        self.aceptarButton.setObjectName(_fromUtf8("aceptarButton"))
        self.cancelarButton = QtGui.QPushButton(Multipasos)
        self.cancelarButton.setGeometry(QtCore.QRect(280, 60, 75, 23))
        self.cancelarButton.setObjectName(_fromUtf8("cancelarButton"))

        self.retranslateUi(Multipasos)
        QtCore.QMetaObject.connectSlotsByName(Multipasos)

    def retranslateUi(self, Multipasos):
        Multipasos.setWindowTitle(_translate("Multipasos", "Múltiples pasos", None))
        self.pasoslabel.setText(_translate("Multipasos", "Número de pasos:", None))
        self.aceptarButton.setText(_translate("Multipasos", "Aceptar", None))
        self.cancelarButton.setText(_translate("Multipasos", "Cancelar", None))

from ..res import oxygen_rc
