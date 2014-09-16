#-*- coding: utf-8 -*-

from plone.app.registry.browser import controlpanel

from ityou.esi.theme.interfaces import IESIThemeSettings, _

class EsiThemeSettingsEditForm(controlpanel.RegistryEditForm):

    schema =        IESIThemeSettings
    label =         _(u"ITYOU ESI settings")
    description =   _(u"""Settings of the ITYOU ESI variables""")

    def updateFields(self):
        super(EsiThemeSettingsEditForm, self).updateFields()


    def updateWidgets(self):
        super(EsiThemeSettingsEditForm, self).updateWidgets()

class EsiThemeSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = EsiThemeSettingsEditForm
