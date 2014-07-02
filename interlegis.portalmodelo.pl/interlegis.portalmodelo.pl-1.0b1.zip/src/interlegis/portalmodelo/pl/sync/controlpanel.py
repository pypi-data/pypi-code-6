# -*- coding: utf-8 -*-
from interlegis.portalmodelo.pl import _
from plone.app.registry.browser import controlpanel
from plone.directives import form
from zope import schema


class ISyncSettings(form.Schema):
    """Interface for the control panel form.
    """
    remote = schema.TextLine(
        title=_(u'SAPL JSON Endpoint'),
        description=_(u'URL to the JSON Endpoint for SAPL.'),
        default=u'',
    )

    path = schema.TextLine(
        title=_(u'Local SAPL Storage'),
        description=_(u'Path to store SAPL information. i.e.: /processo-legislativo'),
        required=True,
        default=u'',
    )


class SyncSettingsEditForm(controlpanel.RegistryEditForm):
    schema = ISyncSettings
    label = _(u'SAPL Sync settings')
    description = _(u'Settings for SAPL Sync Integration.')


class SyncSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SyncSettingsEditForm
