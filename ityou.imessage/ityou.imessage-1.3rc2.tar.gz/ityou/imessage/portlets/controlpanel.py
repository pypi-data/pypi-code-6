#-*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from ityou.imessage.interfaces import IInstantMessageSettings, _

class InstantMessageSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IInstantMessageSettings
    label = _(u"Instant message settings")
    description = _(u"""Settings of the 'imessage' variables
    """)

    def updateFields(self):
        super(InstantMessageSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(InstantMessageSettingsEditForm, self).updateWidgets()

class InstantMessageSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = InstantMessageSettingsEditForm