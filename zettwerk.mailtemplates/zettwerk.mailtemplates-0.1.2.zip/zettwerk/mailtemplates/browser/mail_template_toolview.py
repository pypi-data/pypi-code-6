from zope.component import getUtilitiesFor
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from zettwerk.mailtemplates.interfaces import IMessageTemplateUserFilter
from zettwerk.mailtemplates.interfaces import IMessageTemplateUserObjectFilter


class Imail_template_toolView(Interface):
    """
    mail_template_tool view interface
    """

    def test():
        """ test method"""


class mail_template_toolView(BrowserView):
    """
    mail_template_tool browser view
    """
    implements(Imail_template_toolView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal_groups(self):
        return getToolByName(self.context, 'portal_groups')

    @property
    def templates(self):
        templates = self.context.getFolderContents({'portal_type': 'Template'},
                                                   full_objects=True)
        return sorted(templates, key=lambda template: template.getTemplateId())

    def getGroups(self):
        groups = []
        all_groups = self.portal_groups.listGroups()
        for group in all_groups:
            if group.getId() == 'AuthenticatedUsers':
                continue
            title = group.getProperty('title')
            if not title:
                title = group.getId()
            groups.append((group.getId(), title))
        return groups

    def getExtraFilters(self):
        """ look for registered utilities that might be used as extra
        filters. """
        returner = [{'name': '',
                     'title': ''}]
        checks = getUtilitiesFor(IMessageTemplateUserFilter)
        for check in checks:
            returner.append({'name': check[0],
                             'title': check[1].getTitle(self.request)})
        return returner

    def getExtraObjectFilters(self):
        """ look for registered utilities that might be used as extra
        object filters. """
        returner = []
        checks = getUtilitiesFor(IMessageTemplateUserObjectFilter)
        for check in checks:
            returner.append({'name': check[0],
                             'title': check[1].getTitle(self.request),
                             'objects': check[1].objectList()})
        return returner
