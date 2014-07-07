# -*- coding:utf-8 -*-
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.viewlet.interfaces import IViewlet

from Acquisition import aq_inner
from Products.Five.browser import BrowserView

class ThumbnailViewlet(BrowserView):
    """Viewlet used to display the buttons
    """
    implements(IViewlet)
    render = ViewPageTemplateFile("templates/thumbnail.pt")

    def __init__(self, context, request, view=None, manager=None):
        super(ThumbnailViewlet, self).__init__(context, request)
        self.context = context