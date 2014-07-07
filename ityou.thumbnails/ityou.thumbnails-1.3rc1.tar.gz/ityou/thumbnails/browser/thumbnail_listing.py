# -*- coding: utf-8 -*-
"""Define a browser view for the Archive Text content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""
from Acquisition import aq_inner
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from ZTUtils import Batch
from Products.CMFDefault.browser.utils import ViewBase
from plone.app.content.browser.foldercontents import FolderContentsTable
from zope.component.hooks import getSite

from zope.component import getMultiAdapter

from datetime import datetime, date
from . import isProductAvailable
from ..thumbnail import ThumbnailManager

tm = ThumbnailManager()

class ThumbnailListingView(BrowserView):
    """Listing view with thumbnails and portal actions
    """
    
    html_template = ViewPageTemplateFile('templates/thumbnail_listing.pt')

    def __call__(self):
        """
        Returns Template
        """
        context = aq_inner(self.context)
        context.REQUEST.set('action', 'thumbnail_listing')
        mt = getToolByName(context, "portal_membership")
        self.ESI_ROOT = getSite().absolute_url()
        self.DRAGDROP_INSTALLED = isProductAvailable("ityou.dragdrop")
        if self.DRAGDROP_INSTALLED:
            from ityou.dragdrop.browser.dragdrop import AjaxDragDropView
            dv = AjaxDragDropView(context, context.REQUEST)
            self.CAN_DELETE = dv.canCopyOrMove(context = context, delete = True)
        else:
            self.CAN_DELETE = False
        return self.html_template()
   
    def getFolderContents(self):
        """
        Gets the folder contents and returns them and folder actions.
        Thumbnails come from getThumbnail function of class ThumbnailManager
        returns 
        {
            'id':             'gaga',
            'title':          'GAGA',
            'description':    'This is gaga.',
            'url':            'http://...',          
            'path':           '/inet/inet_documents/...', 
            'thumbnail_url':   'http://.../inet/inet_documents/gaga/@@show_thumbnail', 
            'type':            'document',
            'author':            'Hans Mustermann',
            'created':        '08/05/2013',
            'edited':        '09/05/2013',
            'icon':        Icon of Document Type,
            'content_type_class':    contenttype-folder
             "timestamp_mod"        : obj.created(),
             "timestamp_create"     : obj.modification_date,
        }, 

        """
        context = aq_inner(self.context)
        plone = getMultiAdapter((self.context, self.request), name="plone")
        catalog = getToolByName(context, 'portal_catalog')
        mt = getToolByName(self, 'portal_membership')
        
        folder_path = '/'.join(context.getPhysicalPath())
        brains = catalog(path={'query': folder_path, 'depth': 1}, sort_on='getObjPositionInParent')

        items = []
        for brain in brains:
            obj = brain.getObject()
            author_id = obj.Creator()
            author = mt.getMemberById(author_id)
            if author:
                author_name = author.getProperty("fullname")
            else:
                author_name = author_id
            
            contenttype = obj.portal_type
            contenttype_class = "contenttype-" + contenttype.lower()

            items.append({
                                 "title"            : obj.Title(),
                                 "description"      : obj.Description(),
                                 "url"              : obj.absolute_url(),
                                 "path"             : brain.getURL(relative=True),
                                 "id"               : obj.getId(),
                                 "type"             : brain.Type,
                                 "uid"              : obj.UID(),
                                 "author"           : author_name,
                                 "created"          : context.toLocalizedTime(obj.created()),
                                 "edited"           : context.toLocalizedTime(obj.modification_date),
                                 "icon"             : obj.getIcon(),
                                 "contenttype_class": contenttype_class,
                                 "timestamp_create"        : int(obj.created().timeTime()),
                                 "timestamp_mod"     : int(obj.modification_date.timeTime()),
                                 })
        return { "folder_items" : items}
    
    def canDelete(self):
        """ Checks if user can delete items in current folder
        """
        
    






    
