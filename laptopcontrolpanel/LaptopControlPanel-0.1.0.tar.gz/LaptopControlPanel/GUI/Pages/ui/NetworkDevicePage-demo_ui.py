# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NetworkDevicePage-demo.ui'
#
# Created: Tue May 14 10:51:52 2013
#      by: PyQt4 UI code generator 4.10
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
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(form)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.checkBox = QtGui.QCheckBox(form)
        self.checkBox.setText(_fromUtf8(""))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 3, 1, 1)
        self.checkBox_2 = QtGui.QCheckBox(form)
        self.checkBox_2.setText(_fromUtf8(""))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.gridLayout.addWidget(self.checkBox_2, 1, 2, 1, 1)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.gridLayout)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        form.setWindowTitle(_translate("form", "Form", None))
        self.label.setText(_translate("form", "Wifi", None))
        self.label_2.setText(_translate("form", "Bluetooth", None))
        self.label_3.setText(_translate("form", "hard locked", None))

