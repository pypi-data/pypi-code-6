# -*- coding: utf-8 -*-
import os

from Acquisition import aq_inner
from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from zope.component.hooks import getSite

from .. import THUMBNAIL_HOME, INSTANCE_PATH
from . import DEFAULT_IMAGES_PATH

class ShowThumbnail(BrowserView):
    """
    """
    def __call__(self):
        """
        If a thumbnail of the document (context) exists, this function returns the image,
        it simulates an URL.
        If there's no thumbnail, the function returns None.
        """
        context = aq_inner(self.context)
        size = context.REQUEST.get("size")
        if not size:
            size = ""
        else:
            size = "_" + size
        response = context.REQUEST.RESPONSE
       
        uid = context.UID()
        type = context.portal_type

        tn_uri = THUMBNAIL_HOME + '/' + uid[0:2] + '/' + uid + size + '.png'

        if os.path.isfile(tn_uri):
            f = open(tn_uri, 'r')
            tn = f.read()    
            f.close()
        else:
            if type == 'Folder':                
                thumbnail_path = DEFAULT_IMAGES_PATH + 'folder-thumbnail.png'                 
            else:
                thumbnail_path = DEFAULT_IMAGES_PATH + 'no-thumbnail.png'
            tnf = open(thumbnail_path, 'r')
            tn = tnf.read()
            tnf.close()     
            
        response.setHeader('Content-Type','image/png')
        return tn