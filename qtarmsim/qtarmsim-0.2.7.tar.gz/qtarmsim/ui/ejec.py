# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtarmsim/ui/ejec.ui'
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

class Ui_Ejecutar(object):
    def setupUi(self, Ejecutar):
        Ejecutar.setObjectName(_fromUtf8("Ejecutar"))
        Ejecutar.resize(400, 172)
        self.adress = QtGui.QLineEdit(Ejecutar)
        self.adress.setGeometry(QtCore.QRect(20, 50, 113, 20))
        self.adress.setToolTip(_fromUtf8(""))
        self.adress.setInputMask(_fromUtf8(""))
        self.adress.setObjectName(_fromUtf8("adress"))
        self.adresslabel = QtGui.QLabel(Ejecutar)
        self.adresslabel.setGeometry(QtCore.QRect(20, 20, 88, 31))
        self.adresslabel.setObjectName(_fromUtf8("adresslabel"))
        self.linelabel = QtGui.QLabel(Ejecutar)
        self.linelabel.setGeometry(QtCore.QRect(20, 80, 98, 16))
        self.linelabel.setObjectName(_fromUtf8("linelabel"))
        self.lineEdit = QtGui.QLineEdit(Ejecutar)
        self.lineEdit.setGeometry(QtCore.QRect(20, 100, 113, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.undefcheckBox = QtGui.QCheckBox(Ejecutar)
        self.undefcheckBox.setGeometry(QtCore.QRect(20, 130, 161, 18))
        self.undefcheckBox.setObjectName(_fromUtf8("undefcheckBox"))
        self.aceptarButton = QtGui.QPushButton(Ejecutar)
        self.aceptarButton.setGeometry(QtCore.QRect(280, 40, 75, 23))
        self.aceptarButton.setObjectName(_fromUtf8("aceptarButton"))
        self.cancelarButton = QtGui.QPushButton(Ejecutar)
        self.cancelarButton.setGeometry(QtCore.QRect(280, 90, 75, 23))
        self.cancelarButton.setObjectName(_fromUtf8("cancelarButton"))

        self.retranslateUi(Ejecutar)
        QtCore.QMetaObject.connectSlotsByName(Ejecutar)

    def retranslateUi(self, Ejecutar):
        Ejecutar.setWindowTitle(_translate("Ejecutar", "Parámatros de ejecución", None))
        self.adress.setText(_translate("Ejecutar", "0x00000000", None))
        self.adresslabel.setText(_translate("Ejecutar", "Dirección de inicio:", None))
        self.linelabel.setText(_translate("Ejecutar", "Línea de instrucción:", None))
        self.undefcheckBox.setText(_translate("Ejecutar", "Buscar símbolos no definidos", None))
        self.aceptarButton.setText(_translate("Ejecutar", "Aceptar", None))
        self.cancelarButton.setText(_translate("Ejecutar", "Cancelar", None))

from ..res import oxygen_rc
