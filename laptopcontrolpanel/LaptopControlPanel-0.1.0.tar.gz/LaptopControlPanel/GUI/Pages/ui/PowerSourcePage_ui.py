# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PowerSourcePage.ui'
#
# Created: Thu Sep 18 22:35:31 2014
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

class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName(_fromUtf8("form"))
        form.resize(575, 549)
        self.formLayout = QtGui.QFormLayout(form)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.battery_charge_settings_group_box = QtGui.QGroupBox(form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.battery_charge_settings_group_box.sizePolicy().hasHeightForWidth())
        self.battery_charge_settings_group_box.setSizePolicy(sizePolicy)
        self.battery_charge_settings_group_box.setObjectName(_fromUtf8("battery_charge_settings_group_box"))
        self.formLayout_2 = QtGui.QFormLayout(self.battery_charge_settings_group_box)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.always_charge_battery_check_box = QtGui.QCheckBox(self.battery_charge_settings_group_box)
        self.always_charge_battery_check_box.setObjectName(_fromUtf8("always_charge_battery_check_box"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.always_charge_battery_check_box)
        self.charge_thresholds_group_box = QtGui.QGroupBox(self.battery_charge_settings_group_box)
        self.charge_thresholds_group_box.setObjectName(_fromUtf8("charge_thresholds_group_box"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.charge_thresholds_group_box)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.start_threshold_spin_box = QtGui.QSpinBox(self.charge_thresholds_group_box)
        self.start_threshold_spin_box.setObjectName(_fromUtf8("start_threshold_spin_box"))
        self.gridLayout.addWidget(self.start_threshold_spin_box, 0, 1, 1, 1)
        self.start_label = QtGui.QLabel(self.charge_thresholds_group_box)
        self.start_label.setObjectName(_fromUtf8("start_label"))
        self.gridLayout.addWidget(self.start_label, 0, 0, 1, 1)
        self.stop_threshold_label = QtGui.QLabel(self.charge_thresholds_group_box)
        self.stop_threshold_label.setObjectName(_fromUtf8("stop_threshold_label"))
        self.gridLayout.addWidget(self.stop_threshold_label, 1, 0, 1, 1)
        self.stop_threshold_spin_box = QtGui.QSpinBox(self.charge_thresholds_group_box)
        self.stop_threshold_spin_box.setObjectName(_fromUtf8("stop_threshold_spin_box"))
        self.gridLayout.addWidget(self.stop_threshold_spin_box, 1, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.apply_battery_charge_thresholds_push_button = QtGui.QPushButton(self.charge_thresholds_group_box)
        self.apply_battery_charge_thresholds_push_button.setObjectName(_fromUtf8("apply_battery_charge_thresholds_push_button"))
        self.horizontalLayout.addWidget(self.apply_battery_charge_thresholds_push_button)
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.charge_thresholds_group_box)
        self.error_message_label = QtGui.QLabel(self.battery_charge_settings_group_box)
        self.error_message_label.setObjectName(_fromUtf8("error_message_label"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.error_message_label)
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.battery_charge_settings_group_box)
        self.battery_status_group_box = QtGui.QGroupBox(form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.battery_status_group_box.sizePolicy().hasHeightForWidth())
        self.battery_status_group_box.setSizePolicy(sizePolicy)
        self.battery_status_group_box.setObjectName(_fromUtf8("battery_status_group_box"))
        self.verticalLayout = QtGui.QVBoxLayout(self.battery_status_group_box)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.grid_layout = QtGui.QGridLayout()
        self.grid_layout.setObjectName(_fromUtf8("grid_layout"))
        self.battery_capacity_label = QtGui.QLabel(self.battery_status_group_box)
        self.battery_capacity_label.setIndent(10)
        self.battery_capacity_label.setObjectName(_fromUtf8("battery_capacity_label"))
        self.grid_layout.addWidget(self.battery_capacity_label, 2, 1, 1, 1)
        self.battery_cycle_count_label = QtGui.QLabel(self.battery_status_group_box)
        self.battery_cycle_count_label.setIndent(10)
        self.battery_cycle_count_label.setObjectName(_fromUtf8("battery_cycle_count_label"))
        self.grid_layout.addWidget(self.battery_cycle_count_label, 3, 1, 1, 1)
        self.battery_status_title_label = QtGui.QLabel(self.battery_status_group_box)
        self.battery_status_title_label.setObjectName(_fromUtf8("battery_status_title_label"))
        self.grid_layout.addWidget(self.battery_status_title_label, 1, 0, 1, 1)
        self.battery_capacity_title_label = QtGui.QLabel(self.battery_status_group_box)
        self.battery_capacity_title_label.setObjectName(_fromUtf8("battery_capacity_title_label"))
        self.grid_layout.addWidget(self.battery_capacity_title_label, 2, 0, 1, 1)
        self.ac_status_label = QtGui.QLabel(self.battery_status_group_box)
        self.ac_status_label.setIndent(10)
        self.ac_status_label.setObjectName(_fromUtf8("ac_status_label"))
        self.grid_layout.addWidget(self.ac_status_label, 0, 1, 1, 1)
        self.ac_status_title_label = QtGui.QLabel(self.battery_status_group_box)
        self.ac_status_title_label.setObjectName(_fromUtf8("ac_status_title_label"))
        self.grid_layout.addWidget(self.ac_status_title_label, 0, 0, 1, 1)
        self.battery_cycle_count_title_label = QtGui.QLabel(self.battery_status_group_box)
        self.battery_cycle_count_title_label.setObjectName(_fromUtf8("battery_cycle_count_title_label"))
        self.grid_layout.addWidget(self.battery_cycle_count_title_label, 3, 0, 1, 1)
        self.battery_status_label = QtGui.QLabel(self.battery_status_group_box)
        self.battery_status_label.setMargin(0)
        self.battery_status_label.setIndent(10)
        self.battery_status_label.setObjectName(_fromUtf8("battery_status_label"))
        self.grid_layout.addWidget(self.battery_status_label, 1, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.grid_layout)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.battery_status_group_box)
        self.start_label.setBuddy(self.start_threshold_spin_box)
        self.stop_threshold_label.setBuddy(self.stop_threshold_spin_box)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        form.setWindowTitle(_translate("form", "Form", None))
        self.battery_charge_settings_group_box.setTitle(_translate("form", "Battery Charge Settings", None))
        self.always_charge_battery_check_box.setText(_translate("form", "Allways Charge Battery", None))
        self.charge_thresholds_group_box.setTitle(_translate("form", "Charge Thresholds", None))
        self.start_threshold_spin_box.setSuffix(_translate("form", "%", None))
        self.start_label.setText(_translate("form", "Start", None))
        self.stop_threshold_label.setText(_translate("form", "Stop", None))
        self.stop_threshold_spin_box.setSuffix(_translate("form", "%", None))
        self.apply_battery_charge_thresholds_push_button.setText(_translate("form", "Apply", None))
        self.error_message_label.setText(_translate("form", "Can\'t access ACPI", None))
        self.battery_status_group_box.setTitle(_translate("form", "Battery Status", None))
        self.battery_capacity_label.setText(_translate("form", "80 %", None))
        self.battery_cycle_count_label.setText(_translate("form", "0", None))
        self.battery_status_title_label.setText(_translate("form", "Status", None))
        self.battery_capacity_title_label.setText(_translate("form", "Capacity", None))
        self.ac_status_label.setText(_translate("form", "online", None))
        self.ac_status_title_label.setText(_translate("form", "AC Status", None))
        self.battery_cycle_count_title_label.setText(_translate("form", "Cycle Count", None))
        self.battery_status_label.setText(_translate("form", "Discharging", None))

