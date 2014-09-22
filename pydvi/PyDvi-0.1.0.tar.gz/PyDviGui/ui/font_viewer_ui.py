# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'font_viewer.ui'
#
# Created: Wed Sep 10 12:42:31 2014
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

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName(_fromUtf8("main_window"))
        main_window.resize(800, 600)
        self.central_widget = QtGui.QWidget(main_window)
        self.central_widget.setObjectName(_fromUtf8("central_widget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.central_widget)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.glyph_view_group_box = QtGui.QGroupBox(self.central_widget)
        self.glyph_view_group_box.setObjectName(_fromUtf8("glyph_view_group_box"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.glyph_view_group_box)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.glyph_graphics_view = GlyphGraphicsView(self.glyph_view_group_box)
        self.glyph_graphics_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.glyph_graphics_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.glyph_graphics_view.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing|QtGui.QPainter.SmoothPixmapTransform|QtGui.QPainter.TextAntialiasing)
        self.glyph_graphics_view.setObjectName(_fromUtf8("glyph_graphics_view"))
        self.verticalLayout_2.addWidget(self.glyph_graphics_view)
        self.horizontalLayout_3.addWidget(self.glyph_view_group_box)
        main_window.setCentralWidget(self.central_widget)
        self.dockWidget = QtGui.QDockWidget(main_window)
        self.dockWidget.setFloating(False)
        self.dockWidget.setObjectName(_fromUtf8("dockWidget"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.engine_group_box = QtGui.QGroupBox(self.dockWidgetContents)
        self.engine_group_box.setObjectName(_fromUtf8("engine_group_box"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.engine_group_box)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.pk_radio_button = QtGui.QRadioButton(self.engine_group_box)
        self.pk_radio_button.setChecked(True)
        self.pk_radio_button.setObjectName(_fromUtf8("pk_radio_button"))
        self.verticalLayout_5.addWidget(self.pk_radio_button)
        self.type1_radio_button = QtGui.QRadioButton(self.engine_group_box)
        self.type1_radio_button.setObjectName(_fromUtf8("type1_radio_button"))
        self.verticalLayout_5.addWidget(self.type1_radio_button)
        self.verticalLayout_3.addWidget(self.engine_group_box)
        self.font_information_group_box = QtGui.QGroupBox(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.font_information_group_box.sizePolicy().hasHeightForWidth())
        self.font_information_group_box.setSizePolicy(sizePolicy)
        self.font_information_group_box.setObjectName(_fromUtf8("font_information_group_box"))
        self.verticalLayout = QtGui.QVBoxLayout(self.font_information_group_box)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.font_name_label = QtGui.QLabel(self.font_information_group_box)
        self.font_name_label.setObjectName(_fromUtf8("font_name_label"))
        self.horizontalLayout.addWidget(self.font_name_label)
        self.font_name_line_edit = QtGui.QLineEdit(self.font_information_group_box)
        self.font_name_line_edit.setObjectName(_fromUtf8("font_name_line_edit"))
        self.horizontalLayout.addWidget(self.font_name_line_edit)
        self.load_font_button = QtGui.QPushButton(self.font_information_group_box)
        self.load_font_button.setObjectName(_fromUtf8("load_font_button"))
        self.horizontalLayout.addWidget(self.load_font_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.font_information_table_view = QtGui.QTableView(self.font_information_group_box)
        self.font_information_table_view.setObjectName(_fromUtf8("font_information_table_view"))
        self.verticalLayout.addWidget(self.font_information_table_view)
        self.verticalLayout_3.addWidget(self.font_information_group_box)
        self.glyph_information_group_box = QtGui.QGroupBox(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.glyph_information_group_box.sizePolicy().hasHeightForWidth())
        self.glyph_information_group_box.setSizePolicy(sizePolicy)
        self.glyph_information_group_box.setObjectName(_fromUtf8("glyph_information_group_box"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.glyph_information_group_box)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.char_code_label = QtGui.QLabel(self.glyph_information_group_box)
        self.char_code_label.setObjectName(_fromUtf8("char_code_label"))
        self.horizontalLayout_2.addWidget(self.char_code_label)
        self.char_code_spin_box = QtGui.QSpinBox(self.glyph_information_group_box)
        self.char_code_spin_box.setMaximum(999)
        self.char_code_spin_box.setObjectName(_fromUtf8("char_code_spin_box"))
        self.horizontalLayout_2.addWidget(self.char_code_spin_box)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.glyph_information_table_view = QtGui.QTableView(self.glyph_information_group_box)
        self.glyph_information_table_view.setObjectName(_fromUtf8("glyph_information_table_view"))
        self.verticalLayout_4.addWidget(self.glyph_information_table_view)
        self.verticalLayout_3.addWidget(self.glyph_information_group_box)
        self.dockWidget.setWidget(self.dockWidgetContents)
        main_window.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.about_pydvi_action = QtGui.QAction(main_window)
        self.about_pydvi_action.setObjectName(_fromUtf8("about_pydvi_action"))
        self.about_qt_action = QtGui.QAction(main_window)
        self.about_qt_action.setObjectName(_fromUtf8("about_qt_action"))
        self.about_action = QtGui.QAction(main_window)
        self.about_action.setObjectName(_fromUtf8("about_action"))
        self.help_action = QtGui.QAction(main_window)
        self.help_action.setObjectName(_fromUtf8("help_action"))

        self.retranslateUi(main_window)
        QtCore.QObject.connect(self.font_name_line_edit, QtCore.SIGNAL(_fromUtf8("editingFinished()")), self.load_font_button.click)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(_translate("main_window", "TeX Font Viewer", None))
        self.glyph_view_group_box.setTitle(_translate("main_window", "Glyph View", None))
        self.engine_group_box.setTitle(_translate("main_window", "Engine", None))
        self.pk_radio_button.setText(_translate("main_window", "PK", None))
        self.type1_radio_button.setText(_translate("main_window", "Type1", None))
        self.font_information_group_box.setTitle(_translate("main_window", "Font Information", None))
        self.font_name_label.setText(_translate("main_window", "Font Name", None))
        self.load_font_button.setText(_translate("main_window", "Load", None))
        self.glyph_information_group_box.setTitle(_translate("main_window", "Glyph Information", None))
        self.char_code_label.setText(_translate("main_window", "Char Code", None))
        self.about_pydvi_action.setText(_translate("main_window", "About PyDvi", None))
        self.about_pydvi_action.setToolTip(_translate("main_window", "About PyDvi", None))
        self.about_qt_action.setText(_translate("main_window", "About Qt", None))
        self.about_action.setText(_translate("main_window", "About", None))
        self.about_action.setToolTip(_translate("main_window", "About PyDvi Font Viewer", None))
        self.help_action.setText(_translate("main_window", "Help", None))
        self.help_action.setToolTip(_translate("main_window", "Help", None))

from PyDviGui.FontViewer.GlyphGraphicsView import GlyphGraphicsView
import pydvi_rc
