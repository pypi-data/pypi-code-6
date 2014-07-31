# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ayab_about.ui'
#
# Created by: PyQt4 UI code generator 4.10.3
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(596, 509)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(0, 219, 4148, 14))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 4148, 215))
        font = QtGui.QFont()
        font.setPointSize(144)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.textBrowser = QtGui.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(0, 240, 571, 201))
        self.textBrowser.setAutoFillBackground(True)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 450, 571, 51))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_2.setText(_translate("Form", "All Yarns Are Beautiful", None))
        self.label.setText(_translate("Form", "AYAB", None))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:14px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,Helvetica,sans\'; font-size:11px; color:#000000;\">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce ultricies laoreet neque, id placerat lacus laoreet in. Donec at dui id diam vulputate dignissim ac vitae sem. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sit amet massa tristique mi condimentum accumsan in non tortor. Sed vehicula viverra lectus, sit amet suscipit orci molestie ut. Aenean et gravida erat, non eleifend leo. Vivamus elementum sed ligula vel gravida. Fusce ac tellus id nibh tempor eleifend a id augue. Curabitur faucibus laoreet nunc eget tincidunt. Morbi consequat malesuada purus eu tincidunt. Duis luctus nisi a dolor faucibus, id condimentum turpis eleifend. Aliquam elementum nisi et ante elementum, vitae molestie justo ultrices. Curabitur et consectetur neque.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:14px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,Helvetica,sans\'; font-size:11px; color:#000000;\">Quisque metus arcu, mollis at purus nec, porta mattis orci. Ut consectetur interdum pharetra. Pellentesque quis vestibulum tellus. Etiam dignissim urna a leo ornare faucibus sed eget magna. Duis enim elit, vulputate id lectus ac, posuere tincidunt lacus. Nulla erat libero, commodo vitae malesuada non, feugiat vitae metus. Aenean a velit eget sem tincidunt bibendum.</span></p>\n"
"<a href=\"http://ayab-apparat.net\" > asdf </a> <p style=\" margin-top:0px; margin-bottom:14px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Arial,Helvetica,sans\'; font-size:11px; color:#000000;\">Nam bibendum risus urna, nec mattis neque rhoncus non. Vivamus tempus lectus sed lobortis pharetra. Nunc in orci quis felis pulvinar lobortis. Donec pharetra metus vulputate eros gravida, et posuere orci imperdiet. Curabitur lobortis aliquet tortor, in consequat odio suscipit eget. Curabitur venenatis est ultricies ligula lacinia, quis aliquet eros tempor. Nulla in faucibus est. Maecenas ut congue mauris. Quisque placerat porttitor nisi id dignissim.</span></p></body></html>", None))
        self.pushButton.setText(_translate("Form", "Close", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

