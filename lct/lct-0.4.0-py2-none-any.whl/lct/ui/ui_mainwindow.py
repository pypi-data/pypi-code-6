# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'res\ui\mainwindow.ui'
#
# Created: Mon May 19 19:53:35 2014
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(403, 311)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/moon.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.moonInfoTab = MoonInfoTab()
        self.moonInfoTab.setObjectName(_fromUtf8("moonInfoTab"))
        self.tabWidget.addTab(self.moonInfoTab, _fromUtf8(""))
        self.lunarClubTab = LunarClubTab()
        self.lunarClubTab.setObjectName(_fromUtf8("lunarClubTab"))
        self.tabWidget.addTab(self.lunarClubTab, _fromUtf8(""))
        self.lunarTwoTab = LunarTwoTab()
        self.lunarTwoTab.setObjectName(_fromUtf8("lunarTwoTab"))
        self.tabWidget.addTab(self.lunarTwoTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 403, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuConfigure = QtGui.QMenu(self.menubar)
        self.menuConfigure.setObjectName(_fromUtf8("menuConfigure"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/exit.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon1)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionLocation = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/location.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLocation.setIcon(icon2)
        self.actionLocation.setObjectName(_fromUtf8("actionLocation"))
        self.actionLunarClubTools = QtGui.QAction(MainWindow)
        self.actionLunarClubTools.setObjectName(_fromUtf8("actionLunarClubTools"))
        self.menuFile.addAction(self.actionExit)
        self.menuConfigure.addAction(self.actionLocation)
        self.menuAbout.addAction(self.actionLunarClubTools)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuConfigure.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Lunar Club Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.moonInfoTab), QtGui.QApplication.translate("MainWindow", "Moon Info", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.lunarClubTab), QtGui.QApplication.translate("MainWindow", "Lunar Club", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.lunarTwoTab), QtGui.QApplication.translate("MainWindow", "Lunar II", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuConfigure.setTitle(QtGui.QApplication.translate("MainWindow", "Configure", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setToolTip(QtGui.QApplication.translate("MainWindow", "Exit the program", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLocation.setText(QtGui.QApplication.translate("MainWindow", "Location", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLocation.setToolTip(QtGui.QApplication.translate("MainWindow", "Configure observation location", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLocation.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+L", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLunarClubTools.setText(QtGui.QApplication.translate("MainWindow", "Lunar Club Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLunarClubTools.setToolTip(QtGui.QApplication.translate("MainWindow", "About Lunar Club Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLunarClubTools.setShortcut(QtGui.QApplication.translate("MainWindow", "F1", None, QtGui.QApplication.UnicodeUTF8))

from lct.ui.widgets.lunar_club_tab import LunarClubTab
from lct.ui.widgets.moon_info_tab import MoonInfoTab
from lct.ui.widgets.lunar_two_tab import LunarTwoTab
from . import main_resources_rc
