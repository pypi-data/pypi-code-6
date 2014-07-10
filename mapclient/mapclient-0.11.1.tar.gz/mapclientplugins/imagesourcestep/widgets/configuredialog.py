
'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''
from PySide.QtGui import QDialog, QFileDialog, QDialogButtonBox

from mapclientplugins.imagesourcestep.widgets.ui_configuredialog import Ui_ConfigureDialog
from mapclient.tools.pmr.pmrtool import PMRTool

REQUIRED_STYLE_SHEET = 'border: 1px solid red; border-radius: 3px'
DEFAULT_STYLE_SHEET = 'border: 1px solid gray; border-radius: 3px'

class ConfigureDialogState(object):

    def __init__(self, identifier='', localLocation='', copyTo=False, pmrLocation='', imageType=0, currentTab=0, addToPMR=False, previousLocalLocation=''):
        self._identifier = identifier
        self._localLocation = localLocation
        self._copyTo = copyTo
        self._pmrLocation = pmrLocation
        self._imageType = imageType
        self._currentTab = currentTab
        self._addToPMR = addToPMR
        self._previousLocalLocation = previousLocalLocation


    def location(self):
        if self._localLocation:
            return self._localLocation

        return self._pmrLocation

    def identifier(self):
        return self._identifier

    def setIdentifier(self, identifier):
        self._identifier = identifier

    def copyTo(self):
        return self._copyTo

    def imageType(self):
        return self._imageType

    def currentTab(self):
        return self._currentTab

    def addToPMR(self):
        return self._addToPMR

    def previousLocalLocation(self):
        return self._previousLocalLocation

    def save(self, conf):
        conf.beginGroup('status')
        conf.setValue('identifier', self._identifier)
        conf.setValue('localLocation', self._localLocation)
        conf.setValue('copyTo', self._copyTo)
        conf.setValue('pmrLocation', self._pmrLocation)
        conf.setValue('imageType', self._imageType)
        conf.setValue('currentTab', self._currentTab)
        conf.setValue('addToPMR', self._addToPMR)
        conf.setValue('previousLocalLocation', self._previousLocalLocation)
        conf.endGroup()

    def load(self, conf):
        conf.beginGroup('status')
        self._identifier = conf.value('identifier', '')
        self._localLocation = conf.value('localLocation', '')
        self._copyTo = conf.value('copyTo', 'false') == 'true'
        self._pmrLocation = conf.value('pmrLocation', '')
        self._imageType = int(conf.value('imageType', 0))
        self._currentTab = int(conf.value('currentTab', 0))
        self._addToPMR = conf.value('addToPMR', 'false') == 'true'
        self._previousLocalLocation = conf.value('previousLocalLocation', '')
        conf.endGroup()


class ConfigureDialog(QDialog):
    '''
    Configure dialog to present the user with the options to configure this step.
    '''


    def __init__(self, state, parent=None):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self._ui = Ui_ConfigureDialog()
        self._ui.setupUi(self)

        self.setState(state)
        self._updateUi()
        self.validate()
        self._makeConnections()

    def _makeConnections(self):
        self._ui.identifierLineEdit.textChanged.connect(self.validate)
        self._ui.localLineEdit.textChanged.connect(self._localLocationEdited)
        self._ui.pmrLineEdit.textChanged.connect(self._pmrLocationEdited)
        self._ui.pmrButton.clicked.connect(self._pmrLocationClicked)
        self._ui.localButton.clicked.connect(self._localLocationClicked)
        self._ui.pmrRegisterLabel.linkActivated.connect(self._register)
        self._ui.addToPMRCheckBox.stateChanged.connect(self._updateUi)

    def setState(self, state):
        self._ui.identifierLineEdit.setText(state._identifier)
        self._ui.localLineEdit.setText(state._localLocation)
        self._ui.copyToWorkflowCheckBox.setChecked(state._copyTo)
        self._ui.pmrLineEdit.setText(state._pmrLocation)
        self._ui.imageSourceTypeComboBox.setCurrentIndex(state._imageType)
        self._ui.tabWidget.setCurrentIndex(state._currentTab)
        self._ui.addToPMRCheckBox.setChecked(state._addToPMR)
        self._ui.previousLocationLabel.setText(state._previousLocalLocation)

    def getState(self):
        state = ConfigureDialogState(
            self._ui.identifierLineEdit.text(),
            self._ui.localLineEdit.text(),
            self._ui.copyToWorkflowCheckBox.isChecked(),
            self._ui.pmrLineEdit.text(),
            self._ui.imageSourceTypeComboBox.currentIndex(),
            self._ui.tabWidget.currentIndex(),
            self._ui.addToPMRCheckBox.isChecked(),
            self._ui.previousLocationLabel.text())

        return state

    def _updateUi(self):
        pmr_tool = PMRTool()
        if pmr_tool.hasAccess():
            self._ui.pmrRegisterLabel.hide()

        self._ui.addToPMRCheckBox.setEnabled(pmr_tool.hasAccess())
        if self._ui.addToPMRCheckBox.isChecked():
            self._ui.copyToWorkflowCheckBox.setChecked(True)

    def _register(self):
        pmr_tool = PMRTool()
        pmr_tool.registerWithPMR(self)
        self._updateUi()

    def _pmrLocationClicked(self):
        from mapclient.tools.pmr.pmrsearchdialog import PMRSearchDialog
        dlg = PMRSearchDialog(self)
        dlg.setModal(True)
        if dlg.exec_():
            ws = dlg.getSelectedWorkspace()
            if ws:
                self._ui.pmrLineEdit.setText(ws['target'])

    def _localLocationClicked(self):
        location = QFileDialog.getExistingDirectory(self, 'Select Image File(s) Location', self._ui.previousLocationLabel.text())

        if location:
            self._ui.previousLocationLabel.setText(location)
            self._ui.localLineEdit.setText(location)

    def _pmrLocationEdited(self):
        self._ui.localLineEdit.setText('')
        self.validate()

    def _localLocationEdited(self):
        self._ui.pmrLineEdit.setText('')
        self.validate()

    def localLocation(self):
        return self._ui.localLineEdit.text()

    def copyToWorkflow(self):
        return self._ui.copyToWorkflowCheckBox.isChecked()

    def addToPMR(self):
        return self._ui.addToPMRCheckBox.isChecked()

    def validate(self):
        identifierValid = len(self._ui.identifierLineEdit.text()) > 0
        localValid = len(self._ui.localLineEdit.text()) > 0
        pmrValid = len(self._ui.pmrLineEdit.text()) > 0
        locationValid = localValid or pmrValid
        valid = identifierValid and locationValid

        self._ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid)

        if identifierValid:
            self._ui.identifierLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.identifierLineEdit.setStyleSheet(REQUIRED_STYLE_SHEET)

        if localValid:
            self._ui.localLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.localLineEdit.setStyleSheet(REQUIRED_STYLE_SHEET)

        if pmrValid:
            self._ui.pmrLineEdit.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.pmrLineEdit.setStyleSheet(REQUIRED_STYLE_SHEET)

        return valid


