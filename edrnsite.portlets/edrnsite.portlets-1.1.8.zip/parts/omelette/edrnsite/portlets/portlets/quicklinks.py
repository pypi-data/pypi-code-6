# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EDRN Site's "Quick Links" portlet.'''

from edrnsite.portlets import ProjectMessageFactory as _
from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements

class IQuickLinksPortlet(IPortletDataProvider):
    '''A portlet showing EDRN's quick links.
    '''
    
class Assignment(base.Assignment):
    implements(IQuickLinksPortlet)
    title = _(u'EDRN Quick Links')
    
class Renderer(base.Renderer):
    render = ViewPageTemplateFile('quicklinks.pt')
    
class AddForm(base.NullAddForm):
    def create(self):
        return Assignment()
