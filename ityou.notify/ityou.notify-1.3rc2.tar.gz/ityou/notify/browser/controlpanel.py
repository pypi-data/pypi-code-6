#-*- coding: utf-8 -*-

from plone.app.registry.browser import controlpanel

from ityou.notify.interfaces import INotifySettings, _

class NotifySettingsEditForm(controlpanel.RegistryEditForm):

    schema = INotifySettings
    label = _(u"Notify settings")
    description = _(u"""Setting for the ityou.notiy Product""")

    def updateFields(self):
        super(NotifySettingsEditForm, self).updateFields()


    def updateWidgets(self):
        super(NotifySettingsEditForm, self).updateWidgets()

class NotifySettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NotifySettingsEditForm
