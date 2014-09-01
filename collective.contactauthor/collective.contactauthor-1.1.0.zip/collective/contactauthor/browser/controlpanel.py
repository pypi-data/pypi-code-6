# -*- coding: utf-8 -*-

#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

from z3c.form import button

from plone.app.registry.browser import controlpanel

from collective.contactauthor.interfaces import IAuthorViewProtectionSettings
from collective.contactauthor import messageFactory as _


class ContactAuthorControlPanelEditForm(controlpanel.RegistryEditForm):
    """Contact author settings form"""
    schema = IAuthorViewProtectionSettings
    id = "ContactAuthorControlPanel"
    label = _(u"Contact author settings")
    description = _(u"help_contactauthor_settings_editform",
                    default=u"Manage the message system in the page of author's information")

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"),
                                                      "info")
        self.context.REQUEST.RESPONSE.redirect("@@settings-contactauthor")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))


class ContactAuthorControlPanel(controlpanel.ControlPanelFormWrapper):
    """Contact author control panel"""
    form = ContactAuthorControlPanelEditForm
    #index = ViewPageTemplateFile('controlpanel.pt')
