# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from zope.component import getUtility
try:
    from zope.browsermenu.interfaces import IBrowserMenu
except ImportError:
    from zope.app.publisher.interfaces.browser import IBrowserMenu

from plone.app.layout.viewlets import common
from Products.CMFCore.interfaces import IFolderish
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from . import isProductAvailable
 
class LivesearchViewlet(common.ViewletBase):
    render = ViewPageTemplateFile('templates/livesearch.pt')

class NewContentViewlet(common.ViewletBase):
    render = ViewPageTemplateFile('templates/new_content.pt')

    def has_extuserprofile(self):
        return isProductAvailable("ityou.extuserprofile")

    def menu_home(self):
        """return menue items
        """
        context = aq_inner(self.context)
        menu = getUtility(IBrowserMenu, name='plone_contentmenu')
        mtool = getToolByName(context, "portal_membership")
        amember = mtool.getAuthenticatedMember()
        
        try:
            home_folder = amember.getHomeFolder()
            if home_folder == None:
                return False
        except:
            return False
        
        items = menu.getMenuItems(home_folder, self.request)
        items.reverse()
        
        try:
            add_content_item = items[1]
        except:
            return False
        
        item_info = add_content_item['extra']
        item_id = item_info['id']
        
        if item_id == "plone-contentmenu-factories":
            return items[1]
        else:
            return False

    def menu_here(self):
        """return menue items
        """
        context = aq_inner(self.context)
        menu = getUtility(IBrowserMenu, name='plone_contentmenu')
        obj = context
        container = False
        while not container:
            if IFolderish.providedBy(obj):
                container = obj
            else:
                obj = obj.aq_parent
        items = menu.getMenuItems(container, self.request)

        items.reverse()
        try:
            add_content_item = items[1]
        except:
            return False
        item_info = add_content_item['extra']
        item_id = item_info['id']
        if item_id == "plone-contentmenu-factories":
            return items[1]
        else:
            return False
