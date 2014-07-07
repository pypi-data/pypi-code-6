# -*- coding: utf-8 -*-
import json

from Acquisition import aq_inner
from Products.CMFCore.interfaces._content import IFolderish
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class NavigationView(BrowserView):
    """Get Plone-Navigation items with ajax
        ===> returns json 
    """
    
    def __call__(self):
        """Standard Json view
        """
        context = aq_inner(self.context)
        request = context.REQUEST
        action  = request.get('action')
        path    = request.get('path')

        if action == "get_navigation":
            return self.get_navigation(path)
        else:
            return False

    def get_navigation(self, root_folder=None):
        """Get Sub-Items of object with ajax.
        If path is not given, returns Sub-Items of the context
        ===> returns json
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context,"portal_catalog")        
        if root_folder is None:
            folder_path = '/'.join(context.getPhysicalPath())
        else:
            folder_path = root_folder        

        brains = catalog( path = {'query': folder_path, 'depth': 1})
        items = []

        for brain in brains:
            object = brain.getObject()
            if IFolderish.providedBy(object):
                is_folderish = "is_folderish"
            else:
                is_folderish = "not_folderish"
            if object.aq_parent.getDefaultPage() != "folder_listing" and object.aq_parent.getDefaultPage() is not None:
                standard_view = True
                type = "standard_view"
            else:
                standard_view = False
                type = object.portal_type
            item = {
                    "standard_view" : standard_view,
                    "title"         : object.Title(),
                    "path"          : folder_path,
                    "type"          : type,
                    "is_folderish"  : is_folderish,
                    "absolute_url"  : object.absolute_url()
                     }
            items.append(item)
            ju = JsonApiUtils()
        return ju._json_response( context, items)

class JsonApiUtils():
    """small utilities
    """
    def _json_response(self, context, data):
        """ Returns Json Data in Callback function
        """
        request  = context.REQUEST
        callback = request.get('callback','')        
        request.response.setHeader("Content-type","application/json")
        if callback:
            cb = callback + "(%s);"
            return cb % json.dumps(data)
        else:
            return json.dumps(data)