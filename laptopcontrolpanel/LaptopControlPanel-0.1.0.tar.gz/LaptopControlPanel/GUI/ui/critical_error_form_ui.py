# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'critical_error_form.ui'
#
# Created: Tue Dec 17 21:55:02 2013
#      by: PyQt4 UI code generator 4.10.1
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

class Ui_critical_error_form(object):
    def setupUi(self, critical_error_form):
        critical_error_form.setObjectName(_fromUtf8("critical_error_form"))
        critical_error_form.setWindowModality(QtCore.Qt.ApplicationModal)
        critical_error_form.resize(1057, 683)
        self.verticalLayout_3 = QtGui.QVBoxLayout(critical_error_form)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.error_message_label = QtGui.QLabel(critical_error_form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.error_message_label.sizePolicy().hasHeightForWidth())
        self.error_message_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.error_message_label.setFont(font)
        self.error_message_label.setLineWidth(1)
        self.error_message_label.setTextFormat(QtCore.Qt.RichText)
        self.error_message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_message_label.setObjectName(_fromUtf8("error_message_label"))
        self.verticalLayout_3.addWidget(self.error_message_label)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.show_backtrace_button = QtGui.QPushButton(critical_error_form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_backtrace_button.sizePolicy().hasHeightForWidth())
        self.show_backtrace_button.setSizePolicy(sizePolicy)
        self.show_backtrace_button.setObjectName(_fromUtf8("show_backtrace_button"))
        self.horizontalLayout.addWidget(self.show_backtrace_button)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.back_trace_text_browser = QtGui.QTextEdit(critical_error_form)
        self.back_trace_text_browser.setEnabled(True)
        self.back_trace_text_browser.setMinimumSize(QtCore.QSize(800, 500))
        self.back_trace_text_browser.setDocumentTitle(_fromUtf8(""))
        self.back_trace_text_browser.setReadOnly(True)
        self.back_trace_text_browser.setObjectName(_fromUtf8("back_trace_text_browser"))
        self.verticalLayout_2.addWidget(self.back_trace_text_browser)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.exit_button = QtGui.QPushButton(critical_error_form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit_button.sizePolicy().hasHeightForWidth())
        self.exit_button.setSizePolicy(sizePolicy)
        self.exit_button.setObjectName(_fromUtf8("exit_button"))
        self.verticalLayout.addWidget(self.exit_button)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.ok_button = QtGui.QPushButton(critical_error_form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ok_button.sizePolicy().hasHeightForWidth())
        self.ok_button.setSizePolicy(sizePolicy)
        self.ok_button.setObjectName(_fromUtf8("ok_button"))
        self.verticalLayout.addWidget(self.ok_button)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.retranslateUi(critical_error_form)
        QtCore.QObject.connect(self.ok_button, QtCore.SIGNAL(_fromUtf8("clicked()")), critical_error_form.accept)
        QtCore.QMetaObject.connectSlotsByName(critical_error_form)
        critical_error_form.setTabOrder(self.exit_button, self.ok_button)

    def retranslateUi(self, critical_error_form):
        critical_error_form.setWindowTitle(_translate("critical_error_form", "LaptopControlPanel Critical Error", None))
        self.error_message_label.setText(_translate("critical_error_form", "Error Message", None))
        self.show_backtrace_button.setText(_translate("critical_error_form", "Show Back Trace", None))
        self.back_trace_text_browser.setHtml(_translate("critical_error_form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Back Trace</span></p></body></html>", None))
        self.exit_button.setText(_translate("critical_error_form", "Exit LaptopControlPanel", None))
        self.ok_button.setText(_translate("critical_error_form", "OK", None))

