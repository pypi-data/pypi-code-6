# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'taxonome/gui/ui/nameselector.ui'
#
# Created: Mon Oct 21 09:55:59 2013
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

class Ui_NameSelector(object):
    def setupUi(self, NameSelector):
        NameSelector.setObjectName(_fromUtf8("NameSelector"))
        NameSelector.resize(431, 400)
        self.buttonBox = QtGui.QDialogButtonBox(NameSelector)
        self.buttonBox.setGeometry(QtCore.QRect(80, 360, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.subject_line = QtGui.QLabel(NameSelector)
        self.subject_line.setGeometry(QtCore.QRect(20, 20, 361, 17))
        self.subject_line.setObjectName(_fromUtf8("subject_line"))
        self.choice_list = QtGui.QListView(NameSelector)
        self.choice_list.setGeometry(QtCore.QRect(20, 50, 391, 231))
        self.choice_list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.choice_list.setObjectName(_fromUtf8("choice_list"))
        self.label_3 = QtGui.QLabel(NameSelector)
        self.label_3.setGeometry(QtCore.QRect(20, 300, 331, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.new_name = QtGui.QLineEdit(NameSelector)
        self.new_name.setGeometry(QtCore.QRect(20, 320, 391, 27))
        self.new_name.setObjectName(_fromUtf8("new_name"))
        self.label_3.setBuddy(self.new_name)

        self.retranslateUi(NameSelector)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NameSelector.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NameSelector.reject)
        QtCore.QMetaObject.connectSlotsByName(NameSelector)

    def retranslateUi(self, NameSelector):
        NameSelector.setWindowTitle(_translate("NameSelector", "Select matching name", None))
        self.subject_line.setText(_translate("NameSelector", "Matches for [placeholder]:", None))
        self.label_3.setText(_translate("NameSelector", "Or type another name to find as a &replacement:", None))

