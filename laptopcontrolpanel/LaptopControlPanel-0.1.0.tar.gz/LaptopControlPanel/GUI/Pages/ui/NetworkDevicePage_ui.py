# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NetworkDevicePage.ui'
#
# Created: Thu Sep 18 22:35:30 2014
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

class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName(_fromUtf8("form"))
        form.resize(400, 300)
        self.formLayout = QtGui.QFormLayout(form)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.grid_layout = QtGui.QGridLayout()
        self.grid_layout.setObjectName(_fromUtf8("grid_layout"))
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.grid_layout)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        form.setWindowTitle(_translate("form", "Form", None))

