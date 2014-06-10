# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/leap/bitmask/gui/ui/preferences.ui'
#
# Created: Fri Nov 15 23:53:18 2013
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        Preferences.setObjectName("Preferences")
        Preferences.resize(503, 401)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/mask-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Preferences.setWindowIcon(icon)
        self.gridLayout_3 = QtGui.QGridLayout(Preferences)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 4, 0, 1, 1)
        self.gbPasswordChange = QtGui.QGroupBox(Preferences)
        self.gbPasswordChange.setEnabled(False)
        self.gbPasswordChange.setObjectName("gbPasswordChange")
        self.formLayout = QtGui.QFormLayout(self.gbPasswordChange)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.lblCurrentPassword = QtGui.QLabel(self.gbPasswordChange)
        self.lblCurrentPassword.setObjectName("lblCurrentPassword")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblCurrentPassword)
        self.leCurrentPassword = QtGui.QLineEdit(self.gbPasswordChange)
        self.leCurrentPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.leCurrentPassword.setObjectName("leCurrentPassword")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.leCurrentPassword)
        self.lblNewPassword = QtGui.QLabel(self.gbPasswordChange)
        self.lblNewPassword.setObjectName("lblNewPassword")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblNewPassword)
        self.leNewPassword = QtGui.QLineEdit(self.gbPasswordChange)
        self.leNewPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.leNewPassword.setObjectName("leNewPassword")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.leNewPassword)
        self.lblNewPassword2 = QtGui.QLabel(self.gbPasswordChange)
        self.lblNewPassword2.setObjectName("lblNewPassword2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lblNewPassword2)
        self.leNewPassword2 = QtGui.QLineEdit(self.gbPasswordChange)
        self.leNewPassword2.setEchoMode(QtGui.QLineEdit.Password)
        self.leNewPassword2.setObjectName("leNewPassword2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.leNewPassword2)
        self.pbChangePassword = QtGui.QPushButton(self.gbPasswordChange)
        self.pbChangePassword.setObjectName("pbChangePassword")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.pbChangePassword)
        self.lblPasswordChangeStatus = QtGui.QLabel(self.gbPasswordChange)
        self.lblPasswordChangeStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPasswordChangeStatus.setObjectName("lblPasswordChangeStatus")
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.lblPasswordChangeStatus)
        self.gridLayout_3.addWidget(self.gbPasswordChange, 0, 0, 1, 1)
        self.gbEnabledServices = QtGui.QGroupBox(Preferences)
        self.gbEnabledServices.setObjectName("gbEnabledServices")
        self.gridLayout_2 = QtGui.QGridLayout(self.gbEnabledServices)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pbSaveServices = QtGui.QPushButton(self.gbEnabledServices)
        self.pbSaveServices.setObjectName("pbSaveServices")
        self.gridLayout_2.addWidget(self.pbSaveServices, 3, 1, 1, 1)
        self.gbServices = QtGui.QGroupBox(self.gbEnabledServices)
        self.gbServices.setFlat(False)
        self.gbServices.setObjectName("gbServices")
        self.gridLayout_4 = QtGui.QGridLayout(self.gbServices)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.vlServices = QtGui.QVBoxLayout()
        self.vlServices.setObjectName("vlServices")
        self.gridLayout_4.addLayout(self.vlServices, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.gbServices, 2, 0, 1, 2)
        self.cbProvidersServices = QtGui.QComboBox(self.gbEnabledServices)
        self.cbProvidersServices.setObjectName("cbProvidersServices")
        self.cbProvidersServices.addItem("")
        self.gridLayout_2.addWidget(self.cbProvidersServices, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.gbEnabledServices)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.lblProvidersServicesStatus = QtGui.QLabel(self.gbEnabledServices)
        self.lblProvidersServicesStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.lblProvidersServicesStatus.setObjectName("lblProvidersServicesStatus")
        self.gridLayout_2.addWidget(self.lblProvidersServicesStatus, 1, 0, 1, 2)
        self.gridLayout_3.addWidget(self.gbEnabledServices, 3, 0, 1, 1)
        self.lblCurrentPassword.setBuddy(self.leCurrentPassword)
        self.lblNewPassword.setBuddy(self.leNewPassword)
        self.lblNewPassword2.setBuddy(self.leNewPassword2)

        self.retranslateUi(Preferences)
        QtCore.QMetaObject.connectSlotsByName(Preferences)

    def retranslateUi(self, Preferences):
        Preferences.setWindowTitle(QtGui.QApplication.translate("Preferences", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.gbPasswordChange.setTitle(QtGui.QApplication.translate("Preferences", "Password Change", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCurrentPassword.setText(QtGui.QApplication.translate("Preferences", "&Current password:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblNewPassword.setText(QtGui.QApplication.translate("Preferences", "&New password:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblNewPassword2.setText(QtGui.QApplication.translate("Preferences", "&Re-enter new password:", None, QtGui.QApplication.UnicodeUTF8))
        self.pbChangePassword.setText(QtGui.QApplication.translate("Preferences", "Change", None, QtGui.QApplication.UnicodeUTF8))
        self.lblPasswordChangeStatus.setText(QtGui.QApplication.translate("Preferences", "<Password change status>", None, QtGui.QApplication.UnicodeUTF8))
        self.gbEnabledServices.setTitle(QtGui.QApplication.translate("Preferences", "Enabled services", None, QtGui.QApplication.UnicodeUTF8))
        self.pbSaveServices.setText(QtGui.QApplication.translate("Preferences", "Save this provider settings", None, QtGui.QApplication.UnicodeUTF8))
        self.gbServices.setTitle(QtGui.QApplication.translate("Preferences", "Services", None, QtGui.QApplication.UnicodeUTF8))
        self.cbProvidersServices.setItemText(0, QtGui.QApplication.translate("Preferences", "<Select provider>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Preferences", "Select provider:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblProvidersServicesStatus.setText(QtGui.QApplication.translate("Preferences", "< Providers Services Status >", None, QtGui.QApplication.UnicodeUTF8))

import mainwindow_rc
