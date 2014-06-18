# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res\ui\widgets\lunar_two_tab.ui'
#
# Created: Wed May 07 22:41:49 2014
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LunarTwoTabWidget(object):
    def setupUi(self, LunarTwoTabWidget):
        LunarTwoTabWidget.setObjectName(_fromUtf8("LunarTwoTabWidget"))
        LunarTwoTabWidget.resize(929, 527)
        LunarTwoTabWidget.setWindowTitle(_fromUtf8(""))
        self.horizontalLayout = QtGui.QHBoxLayout(LunarTwoTabWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lunar_two_label = QtGui.QLabel(LunarTwoTabWidget)
        self.lunar_two_label.setObjectName(_fromUtf8("lunar_two_label"))
        self.verticalLayout_2.addWidget(self.lunar_two_label)
        self.lunar_two_tree = QtGui.QTreeWidget(LunarTwoTabWidget)
        self.lunar_two_tree.setMinimumSize(QtCore.QSize(400, 400))
        self.lunar_two_tree.setObjectName(_fromUtf8("lunar_two_tree"))
        self.lunar_two_tree.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout_2.addWidget(self.lunar_two_tree)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(LunarTwoTabWidget)
        QtCore.QMetaObject.connectSlotsByName(LunarTwoTabWidget)

    def retranslateUi(self, LunarTwoTabWidget):
        self.lunar_two_label.setText(QtGui.QApplication.translate("LunarTwoTabWidget", "Features", None, QtGui.QApplication.UnicodeUTF8))

