# -*- coding: utf-8 -*-
import json

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

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
        docs = context.REQUEST.get("order").split(",")
        
        ordering = []
        
        for idx,doc in enumerate(docs):
            obj = reference_tool.lookupObject(doc)
            context.getOrdering().moveObjectToPosition(obj.getId(), idx)
        
        return json.dumps(context.getOrdering().idsInOrder())