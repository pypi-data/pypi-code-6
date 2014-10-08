# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtarmsim/ui/opciones.ui'
#
# Created: Tue Sep  2 17:00:04 2014
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

class Ui_Opciones(object):
    def setupUi(self, Opciones):
        Opciones.setObjectName(_fromUtf8("Opciones"))
        Opciones.resize(400, 300)
        self.actionExplorar = QtGui.QPushButton(Opciones)
        self.actionExplorar.setGeometry(QtCore.QRect(280, 130, 75, 23))
        self.actionExplorar.setObjectName(_fromUtf8("actionExplorar"))
        self.Bare = QtGui.QCheckBox(Opciones)
        self.Bare.setGeometry(QtCore.QRect(41, 51, 99, 18))
        self.Bare.setObjectName(_fromUtf8("Bare"))
        self.Quiet = QtGui.QCheckBox(Opciones)
        self.Quiet.setGeometry(QtCore.QRect(146, 51, 99, 18))
        self.Quiet.setObjectName(_fromUtf8("Quiet"))
        self.Mapped = QtGui.QCheckBox(Opciones)
        self.Mapped.setGeometry(QtCore.QRect(251, 51, 99, 18))
        self.Mapped.setObjectName(_fromUtf8("Mapped"))
        self.Loadtrap = QtGui.QCheckBox(Opciones)
        self.Loadtrap.setGeometry(QtCore.QRect(41, 136, 87, 18))
        self.Loadtrap.setObjectName(_fromUtf8("Loadtrap"))
        self.Directrap = QtGui.QLineEdit(Opciones)
        self.Directrap.setGeometry(QtCore.QRect(134, 135, 133, 20))
        self.Directrap.setObjectName(_fromUtf8("Directrap"))
        self.cancelarButton = QtGui.QPushButton(Opciones)
        self.cancelarButton.setGeometry(QtCore.QRect(290, 240, 75, 23))
        self.cancelarButton.setObjectName(_fromUtf8("cancelarButton"))
        self.buttonBox = QtGui.QPushButton(Opciones)
        self.buttonBox.setGeometry(QtCore.QRect(190, 240, 75, 23))
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(Opciones)
        QtCore.QMetaObject.connectSlotsByName(Opciones)

    def retranslateUi(self, Opciones):
        Opciones.setWindowTitle(_translate("Opciones", "Opciones", None))
        self.actionExplorar.setText(_translate("Opciones", "Explorar", None))
        self.Bare.setText(_translate("Opciones", "Bare mode", None))
        self.Quiet.setText(_translate("Opciones", "Quiet mode", None))
        self.Mapped.setText(_translate("Opciones", "Mapped I/O", None))
        self.Loadtrap.setText(_translate("Opciones", "Load trap file", None))
        self.cancelarButton.setText(_translate("Opciones", "Cancelar", None))
        self.buttonBox.setText(_translate("Opciones", "Aceptar", None))

from ..res import oxygen_rc
