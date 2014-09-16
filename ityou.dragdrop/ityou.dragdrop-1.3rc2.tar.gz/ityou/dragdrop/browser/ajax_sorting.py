# -*- coding: utf-8 -*-
import json
import logging

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.app.uuid.utils import uuidToObject

class AjaxSorting(BrowserView):
    """ Sorts the given documents 
    """
    def __call__(self):
        """ When called it iterates over the documents and sets new sorting numbers
        Parameters: "order" = uid,uid,uid
        
        Returns: Ordering (list of ids)
        """
        context = aq_inner(self.context)
        reference_tool = getToolByName(self, 'reference_catalog')
        uids = context.REQUEST.get("order").split(",")
        print "uids:", uids
        ordering = []
        
        for idx,uid in enumerate(uids):
            obj = uuidToObject(uid)
            if obj:
                try:
                    context.getOrdering().moveObjectToPosition(obj.getId(), idx)
                except:
                    logging.warning('Could not sort folder items!')
        
        return json.dumps( context.getOrdering().idsInOrder() )
