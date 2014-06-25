# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/pmrhgcommitdialog.ui'
#
# Created: Wed Dec  4 17:01:10 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PMRHgCommitDialog(object):
    def setupUi(self, PMRHgCommitDialog):
        PMRHgCommitDialog.setObjectName("PMRHgCommitDialog")
        PMRHgCommitDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(PMRHgCommitDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtGui.QGroupBox(PMRHgCommitDialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.commentTextEdit = QtGui.QPlainTextEdit(self.groupBox)
        self.commentTextEdit.setObjectName("commentTextEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.commentTextEdit)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(PMRHgCommitDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_3.setBuddy(self.commentTextEdit)

        self.retranslateUi(PMRHgCommitDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), PMRHgCommitDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PMRHgCommitDialog)
        PMRHgCommitDialog.setTabOrder(self.commentTextEdit, self.buttonBox)

    def retranslateUi(self, PMRHgCommitDialog):
        PMRHgCommitDialog.setWindowTitle(QtGui.QApplication.translate("PMRHgCommitDialog", "PMR Workspace Commit", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PMRHgCommitDialog", "PMR Workspace Commit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PMRHgCommitDialog", "comment:", None, QtGui.QApplication.UnicodeUTF8))
        self.commentTextEdit.setPlainText(QtGui.QApplication.translate("PMRHgCommitDialog", "Lazy commit message from MAP Client.", None, QtGui.QApplication.UnicodeUTF8))

