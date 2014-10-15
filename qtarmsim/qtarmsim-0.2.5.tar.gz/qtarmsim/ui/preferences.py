# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtarmsim/ui/preferences.ui'
#
# Created: Tue Sep  2 17:00:02 2014
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

class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        PreferencesDialog.setObjectName(_fromUtf8("PreferencesDialog"))
        PreferencesDialog.resize(660, 388)
        self.verticalLayout = QtGui.QVBoxLayout(PreferencesDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(PreferencesDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabARMSim = QtGui.QWidget()
        self.tabARMSim.setObjectName(_fromUtf8("tabARMSim"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tabARMSim)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.groupBox = QtGui.QGroupBox(self.tabARMSim)
        self.groupBox.setTitle(_fromUtf8("ARMSim"))
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelARMSimCommand = QtGui.QLabel(self.groupBox)
        self.labelARMSimCommand.setObjectName(_fromUtf8("labelARMSimCommand"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.labelARMSimCommand)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEditARMSimDirectory = QtGui.QLineEdit(self.groupBox)
        self.lineEditARMSimDirectory.setText(_fromUtf8(""))
        self.lineEditARMSimDirectory.setObjectName(_fromUtf8("lineEditARMSimDirectory"))
        self.horizontalLayout.addWidget(self.lineEditARMSimDirectory)
        self.toolButtonARMSimDirectory = QtGui.QToolButton(self.groupBox)
        self.toolButtonARMSimDirectory.setObjectName(_fromUtf8("toolButtonARMSimDirectory"))
        self.horizontalLayout.addWidget(self.toolButtonARMSimDirectory)
        self.formLayout.setLayout(4, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEditARMSimCommand = QtGui.QLineEdit(self.groupBox)
        self.lineEditARMSimCommand.setObjectName(_fromUtf8("lineEditARMSimCommand"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEditARMSimCommand)
        self.labelARMSimServer = QtGui.QLabel(self.groupBox)
        self.labelARMSimServer.setObjectName(_fromUtf8("labelARMSimServer"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelARMSimServer)
        self.lineEditARMSimServer = QtGui.QLineEdit(self.groupBox)
        self.lineEditARMSimServer.setText(_fromUtf8(""))
        self.lineEditARMSimServer.setObjectName(_fromUtf8("lineEditARMSimServer"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditARMSimServer)
        self.labelARMSimPort = QtGui.QLabel(self.groupBox)
        self.labelARMSimPort.setObjectName(_fromUtf8("labelARMSimPort"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelARMSimPort)
        self.spinBoxARMSimPort = QtGui.QSpinBox(self.groupBox)
        self.spinBoxARMSimPort.setMinimum(8000)
        self.spinBoxARMSimPort.setMaximum(9999)
        self.spinBoxARMSimPort.setProperty("value", 8010)
        self.spinBoxARMSimPort.setObjectName(_fromUtf8("spinBoxARMSimPort"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.spinBoxARMSimPort)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.tabARMSim)
        self.groupBox_2.setTitle(_fromUtf8("GCC ARM"))
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.lineEditARMGccOptions = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditARMGccOptions.setText(_fromUtf8(""))
        self.lineEditARMGccOptions.setObjectName(_fromUtf8("lineEditARMGccOptions"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditARMGccOptions)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEditARMGccCommand = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditARMGccCommand.setText(_fromUtf8(""))
        self.lineEditARMGccCommand.setObjectName(_fromUtf8("lineEditARMGccCommand"))
        self.horizontalLayout_2.addWidget(self.lineEditARMGccCommand)
        self.toolButtonARMGccCommand = QtGui.QToolButton(self.groupBox_2)
        self.toolButtonARMGccCommand.setObjectName(_fromUtf8("toolButtonARMGccCommand"))
        self.horizontalLayout_2.addWidget(self.toolButtonARMGccCommand)
        self.formLayout_2.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.labelARMGccOptions = QtGui.QLabel(self.groupBox_2)
        self.labelARMGccOptions.setObjectName(_fromUtf8("labelARMGccOptions"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelARMGccOptions)
        self.labelARMGccCommand = QtGui.QLabel(self.groupBox_2)
        self.labelARMGccCommand.setObjectName(_fromUtf8("labelARMGccCommand"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelARMGccCommand)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        spacerItem = QtGui.QSpacerItem(20, 43, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.pushButtonARMSimRestoreDefaults = QtGui.QPushButton(self.tabARMSim)
        self.pushButtonARMSimRestoreDefaults.setObjectName(_fromUtf8("pushButtonARMSimRestoreDefaults"))
        self.horizontalLayout_3.addWidget(self.pushButtonARMSimRestoreDefaults)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tabARMSim, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(PreferencesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PreferencesDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PreferencesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PreferencesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PreferencesDialog)

    def retranslateUi(self, PreferencesDialog):
        PreferencesDialog.setWindowTitle(_translate("PreferencesDialog", "Qt ARMSim Preferences", None))
        self.labelARMSimCommand.setText(_translate("PreferencesDialog", "ARMSim directory", None))
        self.toolButtonARMSimDirectory.setText(_translate("PreferencesDialog", "...", None))
        self.label.setText(_translate("PreferencesDialog", "Command line", None))
        self.labelARMSimServer.setText(_translate("PreferencesDialog", "Server", None))
        self.labelARMSimPort.setText(_translate("PreferencesDialog", "Port", None))
        self.toolButtonARMGccCommand.setText(_translate("PreferencesDialog", "...", None))
        self.labelARMGccOptions.setText(_translate("PreferencesDialog", "Options", None))
        self.labelARMGccCommand.setText(_translate("PreferencesDialog", "Command line", None))
        self.pushButtonARMSimRestoreDefaults.setText(_translate("PreferencesDialog", "Restore Defaults", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabARMSim), _translate("PreferencesDialog", "ARMSim", None))

from ..res import oxygen_rc
