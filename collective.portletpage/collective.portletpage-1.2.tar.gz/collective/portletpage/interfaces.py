# -*- coding: utf-8 -*-
from collective.portletpage import MessageFactory as _
from plone.app.portlets.interfaces import IColumn
from plone.portlets.interfaces import IPortletManager
from zope import schema
from zope.interface import Interface


class IPortletPage(Interface):
    """Content type interface for portlet pages
    """
    title = schema.TextLine(title=_(u"Page title"))
    text = schema.Text(title=_(u"Body text"))


class IPortletPageColumn(IPortletManager, IColumn):
    """Marker interface describing columns on a portlet page
    """
