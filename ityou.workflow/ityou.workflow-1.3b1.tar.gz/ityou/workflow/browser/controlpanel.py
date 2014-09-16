#-*- coding: utf-8 -*-

from plone.app.registry.browser import controlpanel
from .. import INDEX, INDEX_OFF, TODO, TODO_TITLE
from ityou.workflow.interfaces import IWorkflowSettings, _
from Acquisition import aq_inner
import logging
from z3c.form import button
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName

from exceptions import AttributeError

from ..interfaces import IWorkflowSettings
from .. import _

class WorkflowSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IWorkflowSettings
    label = _(u"Workflow settings")
    description = _(u"""Settings of the workflow product variables""")

    def updateFields(self):
        super(WorkflowSettingsEditForm, self).updateFields()


    def updateWidgets(self):
        super(WorkflowSettingsEditForm, self).updateWidgets()

    @button.buttonAndHandler(_(u"Save"), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved."), "info")
        
        # --------- changes default Members View and rename index_html ------------------------
        if data['todo_enabled'] == True:
            self._set_todo_view()
        else:
            self._reset_todo_view()
                  
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(), self.control_panel_view))

    @button.buttonAndHandler(_(u"Cancel"), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled."), "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(), self.control_panel_view))

    def _set_todo_view(self):
        """We have to change the default view for the todo folder to @@todo
           and to rename index_html to index_html_OFF
           If there's no todo folder, it is created
        """
        context = aq_inner(self.context)
        ut = getToolByName(context, "portal_url")
        mt = getToolByName(context, 'portal_membership')
        portal = ut.getPortalObject()
        
        try:
            todo_folder = getattr(portal, TODO)
        except:
            portal.invokeFactory("Folder", TODO)
            todo_folder = getattr(portal, TODO)
            todo_folder.setTitle(self.context.translate(TODO_TITLE))
            todo_folder.reindexObject()
            
        if todo_folder.getLayout() !=  '@@todo':
            todo_folder.setLayout('@@todo')
            logging.info( "Set layout to %s" % todo_folder.getLayout())

        try:
            todo_folder.manage_renameObject(INDEX, INDEX_OFF)
            logging.info( "Renamed %s to %s" % (INDEX, INDEX_OFF) )
        except ValueError:
            logging.info( "No %s available" % (INDEX) )
       

    def _reset_todo_view(self):
        """set default layout to folder_listing and index_html_OFF to index_html
        """
        context = aq_inner(self.context)
        mt      = getToolByName(context, 'portal_membership')
        ut = getToolByName(context, "portal_url")
        portal = ut.getPortalObject()
        todo_folder = getattr(portal, TODO)
        
        if todo_folder.getLayout() ==  '@@todo':
            todo_folder.setLayout('folder_listing')
            logging.info( "Reset layout to %s" % todo_folder.getLayout())

        if hasattr(todo_folder,INDEX_OFF):
            todo_folder.manage_renameObject(INDEX_OFF, INDEX)
            logging.info( "Renamed %s to %s" % (INDEX_OFF, INDEX) )

class WorkflowSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = WorkflowSettingsEditForm
