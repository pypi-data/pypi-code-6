# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtarmsim/ui/value.ui'
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

class Ui_Value(object):
    def setupUi(self, Value):
        Value.setObjectName(_fromUtf8("Value"))
        Value.resize(400, 142)
        self.direcLabel = QtGui.QLabel(Value)
        self.direcLabel.setGeometry(QtCore.QRect(20, 20, 151, 16))
        self.direcLabel.setObjectName(_fromUtf8("direcLabel"))
        self.direcLineEdit = QtGui.QLineEdit(Value)
        self.direcLineEdit.setGeometry(QtCore.QRect(20, 40, 201, 20))
        self.direcLineEdit.setObjectName(_fromUtf8("direcLineEdit"))
        self.valueLabel = QtGui.QLabel(Value)
        self.valueLabel.setGeometry(QtCore.QRect(20, 80, 46, 14))
        self.valueLabel.setObjectName(_fromUtf8("valueLabel"))
        self.valueLineEdit = QtGui.QLineEdit(Value)
        self.valueLineEdit.setGeometry(QtCore.QRect(20, 100, 201, 20))
        self.valueLineEdit.setObjectName(_fromUtf8("valueLineEdit"))
        self.aceptarButton = QtGui.QPushButton(Value)
        self.aceptarButton.setGeometry(QtCore.QRect(290, 20, 75, 23))
        self.aceptarButton.setObjectName(_fromUtf8("aceptarButton"))
        self.cancelarButton = QtGui.QPushButton(Value)
        self.cancelarButton.setGeometry(QtCore.QRect(290, 60, 75, 23))
        self.cancelarButton.setObjectName(_fromUtf8("cancelarButton"))

        self.retranslateUi(Value)
        QtCore.QMetaObject.connectSlotsByName(Value)

    def retranslateUi(self, Value):
        Value.setWindowTitle(_translate("Value", "Asignar valor a registro", None))
        self.direcLabel.setText(_translate("Value", "Dirección o nombre de registro:", None))
        self.valueLabel.setText(_translate("Value", "Valor:", None))
        self.aceptarButton.setText(_translate("Value", "Aceptar", None))
        self.cancelarButton.setText(_translate("Value", "Cancelar", None))

from ..res import oxygen_rc
