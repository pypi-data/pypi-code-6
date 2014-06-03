# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter


class Base(BrowserView):
    """Base class for index page views
    """
    @memoize
    def plone_view(self):
        return getMultiAdapter((self.context, self.request), name=u"plone")


class TwoColumns(Base):
    """A two-column layout.
    """
    __call__ = ViewPageTemplateFile('two-columns.pt')

    def hasColumnTop(self):
        ploneview = self.plone_view()
        return ploneview.have_portlets('collective.portletpage.toprow', view=self)

    def hasColumnFirst(self):
        ploneview = self.plone_view()
        return ploneview.have_portlets('collective.portletpage.firstcolumn', view=self)

    def hasColumnSecond(self):
        ploneview = self.plone_view()
        return ploneview.have_portlets('collective.portletpage.secondcolumn', view=self)

    def hasColumnBottom(self):
        ploneview = self.plone_view()
        return ploneview.have_portlets('collective.portletpage.bottomrow', view=self)
