# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtarmsim/ui/imprimir.ui'
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

class Ui_Imprimir(object):
    def setupUi(self, Imprimir):
        Imprimir.setObjectName(_fromUtf8("Imprimir"))
        Imprimir.resize(400, 300)
        self.aceptarButton = QtGui.QPushButton(Imprimir)
        self.aceptarButton.setGeometry(QtCore.QRect(300, 30, 75, 23))
        self.aceptarButton.setObjectName(_fromUtf8("aceptarButton"))
        self.cancelarButton = QtGui.QPushButton(Imprimir)
        self.cancelarButton.setGeometry(QtCore.QRect(300, 70, 75, 23))
        self.cancelarButton.setObjectName(_fromUtf8("cancelarButton"))
        self.comboBox = QtGui.QComboBox(Imprimir)
        self.comboBox.setGeometry(QtCore.QRect(30, 40, 181, 21))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.labelFrom = QtGui.QLabel(Imprimir)
        self.labelFrom.setGeometry(QtCore.QRect(30, 110, 46, 14))
        self.labelFrom.setObjectName(_fromUtf8("labelFrom"))
        self.Tolabel = QtGui.QLabel(Imprimir)
        self.Tolabel.setGeometry(QtCore.QRect(30, 170, 46, 14))
        self.Tolabel.setObjectName(_fromUtf8("Tolabel"))
        self.fromEdit = QtGui.QLineEdit(Imprimir)
        self.fromEdit.setEnabled(False)
        self.fromEdit.setGeometry(QtCore.QRect(30, 130, 121, 20))
        self.fromEdit.setObjectName(_fromUtf8("fromEdit"))
        self.toEdit = QtGui.QLineEdit(Imprimir)
        self.toEdit.setEnabled(False)
        self.toEdit.setGeometry(QtCore.QRect(30, 190, 121, 20))
        self.toEdit.setObjectName(_fromUtf8("toEdit"))

        self.retranslateUi(Imprimir)
        QtCore.QMetaObject.connectSlotsByName(Imprimir)

    def retranslateUi(self, Imprimir):
        Imprimir.setWindowTitle(_translate("Imprimir", "Imprimir valor", None))
        self.aceptarButton.setText(_translate("Imprimir", "Aceptar", None))
        self.cancelarButton.setText(_translate("Imprimir", "Cancelar", None))
        self.labelFrom.setText(_translate("Imprimir", "From:", None))
        self.Tolabel.setText(_translate("Imprimir", "to:", None))

from ..res import oxygen_rc
