#-*- coding: utf-8 -*-

from plone.app.registry.browser import controlpanel

from ityou.thumbnails.interfaces import IThumbnailSettings, _

class ThumbnailSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IThumbnailSettings
    label = _(u"Thumbnail settings")
    description = _(u"""Settings of thumbnail variables
    """)

    def updateFields(self):
        super(ThumbnailSettingsEditForm, self).updateFields()


    def updateWidgets(self):
        super(ThumbnailSettingsEditForm, self).updateWidgets()

class ThumbnailSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ThumbnailSettingsEditForm