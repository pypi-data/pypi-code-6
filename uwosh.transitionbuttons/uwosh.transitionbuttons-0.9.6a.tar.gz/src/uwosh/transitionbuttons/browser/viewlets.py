from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from uwosh.transitionbuttons.interfaces import IButtonSettings

from AccessControl.PermissionRole import rolesForPermissionOn

from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from string import split
import json

class ButtonViewlet(ViewletBase):
    render = ViewPageTemplateFile('js_viewlet.pt')
    settings = []

    def isPanelDisabled(self):

        memTool = getToolByName(self, 'portal_membership')
        user = memTool.getAuthenticatedMember()
        res = user.getProperty('buttonsDisabled')

        # If the current content type isn't enabled, stop here
        settings = self.getSettings()
        types = settings.EnabledTypes
        if types:
            if self.context.portal_type not in types:
                return False

        if( res == False or res == True ):
            return not res

    # gets the settings from the add-on control panel
    def getSettings(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IButtonSettings, False)
        return settings

    def getWFState(self):
        wf_tool = getToolByName(self, 'portal_workflow')

        try:
            state = wf_tool.getInfoFor(self.context, 'review_state')
            return state
        except:
            return False

    def getStateDescription(self):

        wf_tool = getToolByName(self, 'portal_workflow')
        defaultWorkflow = wf_tool.getChainForPortalType(self.context.portal_type)

        state = self.getWFState()

        if not wf_tool:
            return False

        if not defaultWorkflow:
            return False

        try:
            # defaultWorkflow is a tuple, so we need to take the index of it
            # 
            # TODO: fix for sites with multiple simultaneous workflows?
            desc = wf_tool[ defaultWorkflow[0] ].states[state].description
        except:
            return False

        return desc

    def getTransitions(self):

        wf_tool = getToolByName(self, 'portal_workflow')
        defaultWorkflow = wf_tool.getChainForPortalType(self.context)

        transitions = wf_tool[ defaultWorkflow[0] ].transitions
        transitionList = [];

        if transitions:
            for transition in transitions:
                transitionList.append(transition)

            return transitionList
        else:
            return False

    def getSite(self):
        return self.context.portal_url()

    def getPreferencesUrl(self):
        base = self.getSite()
        base += '/@@personal-preferences'

        return base

    def setJson(self):

        panelSettings = self.getSettings()

        settings = {}
        settings["isPanelDisabled"] = self.isPanelDisabled()
        settings["allowedTransitions"] = self.getTransitions()
        settings["wfState"] = self.getWFState() 
        settings["stateDescription"] = self.getStateDescription()
        settings["pageElement"] = panelSettings.pageElement
        settings["floating"] = panelSettings.floating
        settings["preferencesUrl"] = self.getPreferencesUrl()

        return json.dumps(settings, sort_keys=False)

    def update(self):

        self.buttonJson = self.setJson()

