# -*- coding: utf-8 -*-
import json

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from ..thumbnail import ThumbnailManager

tm = ThumbnailManager()

class AjaxGetThumbnail(BrowserView):
    """ Returns Thumbnail after possible generation of it 
    """
    def __call__(self):
        """ Calls getThumbnail function and returns as json
        """
        context = aq_inner(self.context)
        size = context.REQUEST.get("size")
        caching = context.REQUEST.get("caching") or False
        if not size:
            size = ""
        if caching:
            thumb = tm.getCachedThumbnail(self.context, size = size)
        else:
            thumb = tm.getThumbnail(self.context, size = size)
        return json.dumps(thumb)
