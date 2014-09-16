# -*- coding: utf-8 -*-
## -----------------------------------------------------------------
## Copyright (C)2013 ITYOU - www.ityou.de - support@ityou.de
## -----------------------------------------------------------------
"""
Only for testing
"""
from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from Products.CMFCore.permissions import ModifyPortalContent, AddPortalContent
     
class CheckPermissionsView(BrowserView):
    """ Test Permissions
    """

    def __call__(self):

        context = aq_inner(self.context)
        request = context.REQUEST        
        sm =      getSecurityManager()

        print "------------------"
        print context.title_or_id()
        print sm.checkPermission(AddPortalContent, context)

        return         
    

