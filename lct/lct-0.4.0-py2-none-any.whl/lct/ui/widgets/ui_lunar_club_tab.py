# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res\ui\widgets\lunar_club_tab.ui'
#
# Created: Sun May 18 21:26:19 2014
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LunarClubTabWidget(object):
    def setupUi(self, LunarClubTabWidget):
        LunarClubTabWidget.setObjectName(_fromUtf8("LunarClubTabWidget"))
        LunarClubTabWidget.resize(833, 447)
        LunarClubTabWidget.setWindowTitle(_fromUtf8(""))
        self.horizontalLayout = QtGui.QHBoxLayout(LunarClubTabWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lunarClubSpecialWidget = LunarClubSpecialWidget(LunarClubTabWidget)
        self.lunarClubSpecialWidget.setObjectName(_fromUtf8("lunarClubSpecialWidget"))
        self.horizontalLayout.addWidget(self.lunarClubSpecialWidget)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lunar_club_label = QtGui.QLabel(LunarClubTabWidget)
        self.lunar_club_label.setObjectName(_fromUtf8("lunar_club_label"))
        self.verticalLayout.addWidget(self.lunar_club_label)
        self.lunar_club_tree = QtGui.QTreeWidget(LunarClubTabWidget)
        self.lunar_club_tree.setMinimumSize(QtCore.QSize(400, 400))
        self.lunar_club_tree.setObjectName(_fromUtf8("lunar_club_tree"))
        self.lunar_club_tree.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout.addWidget(self.lunar_club_tree)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(LunarClubTabWidget)
        QtCore.QMetaObject.connectSlotsByName(LunarClubTabWidget)

    def retranslateUi(self, LunarClubTabWidget):
        self.lunar_club_label.setText(QtGui.QApplication.translate("LunarClubTabWidget", "Features", None, QtGui.QApplication.UnicodeUTF8))

from lct.ui.widgets.lunar_club_special_widget import LunarClubSpecialWidget
