# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GpuPage.ui'
#
# Created: Thu Sep 18 22:35:31 2014
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
        form.resize(575, 549)
        self.formLayout = QtGui.QFormLayout(form)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.on_off_button = QtGui.QPushButton(form)
        self.on_off_button.setObjectName(_fromUtf8("on_off_button"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.on_off_button)
        self.nvidia_gpu_title_label = QtGui.QLabel(form)
        self.nvidia_gpu_title_label.setObjectName(_fromUtf8("nvidia_gpu_title_label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.nvidia_gpu_title_label)
        self.nvidia_gpu_title_label.setBuddy(self.on_off_button)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        form.setWindowTitle(_translate("form", "Form", None))
        self.on_off_button.setText(_translate("form", "ON", None))
        self.nvidia_gpu_title_label.setText(_translate("form", "Nvidia GPU", None))

