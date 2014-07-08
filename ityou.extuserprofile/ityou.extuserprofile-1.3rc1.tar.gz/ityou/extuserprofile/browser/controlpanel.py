#-*- coding: utf-8 -*-
import logging
from Acquisition import aq_inner
from z3c.form import button

from zope.component.hooks import getSite

from plone.app.registry.browser import controlpanel

from Products.statusmessages.interfaces import IStatusMessage

from Products.CMFCore.utils import getToolByName

from ..interfaces import IExtUserProfileSettings, _
from .. import INDEX, INDEX_OFF

class ExtUserProfileSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IExtUserProfileSettings
    label = _(u"User extended profile settings")
    description = _(u"""Settings of the user extended profile variables
    """)

    def updateFields(self):
        super(ExtUserProfileSettingsEditForm, self).updateFields()


    def updateWidgets(self):
        super(ExtUserProfileSettingsEditForm, self).updateWidgets()

    @button.buttonAndHandler(_(u"Save"), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved."), "info")
        
        # --------- changes default Members View and rename index_html ------------------------
        if data['extuserprofile_enabled'] == True:
            self._set_memberfolder_view()
        else:
            self._reset_memberfolder_view()
                  
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(), self.control_panel_view))

    @button.buttonAndHandler(_(u"Cancel"), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled."), "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(), self.control_panel_view))

    def _set_memberfolder_view(self):
        """We have to change the default view for the main memberfolder to @@users
           and to rename index_html to index_html_OFF
           (@LM: think off reinstalling index_html when uninstalling and disabling the
           extuserprofile!!)
        """
        context = aq_inner(self.context)
        mt      = getToolByName(context, 'portal_membership')
        mfolder = mt.getMembersFolder()
        
        if mfolder.getLayout() !=  '@@users':
            mfolder.setLayout('@@users')
            logging.info( "Set layout to %s" % mfolder.getLayout())

        if hasattr(mfolder,INDEX):
            mfolder.manage_renameObject(INDEX, INDEX_OFF)
            logging.info( "Renamed %s to %s" % (INDEX, INDEX_OFF) )
       

    def _reset_memberfolder_view(self):
        """set default layout to folder_listing and index_html_OFF to index_html
        """
        context = aq_inner(self.context)
        mt      = getToolByName(context, 'portal_membership')
        mfolder = mt.getMembersFolder()
        
        if mfolder.getLayout() ==  '@@users':
            mfolder.setLayout('folder_listing')
            logging.info( "Reset layout to %s" % mfolder.getLayout())

        if hasattr(mfolder,INDEX_OFF):
            mfolder.manage_renameObject(INDEX_OFF, INDEX)
            logging.info( "Renamed %s to %s" % (INDEX_OFF, INDEX) )
       


class ExtUserProfileSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ExtUserProfileSettingsEditForm
