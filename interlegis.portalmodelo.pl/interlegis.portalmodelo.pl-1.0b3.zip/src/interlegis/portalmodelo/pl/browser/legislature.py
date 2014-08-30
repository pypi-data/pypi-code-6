# -*- coding: utf-8 -*-

from five import grok
from interlegis.portalmodelo.pl import _
from interlegis.portalmodelo.pl.interfaces import ILegislature
from interlegis.portalmodelo.pl.utils import _get_legislatures
from plone import api
from plone.directives import dexterity
from Products.CMFCore.interfaces import IFolderish

grok.templatedir('templates')


class Legislature_View(dexterity.DisplayForm):
    grok.context(ILegislature)
    grok.require('zope2.View')
    grok.name('view')

    def parliamentarians(self):
        """Return list of parliamentarians of the legislature.
        """
        results = []
        for member in self.context.members:
            obj = member.to_object
            results.append(dict(
                full_name=obj.full_name,
                url=obj.absolute_url(),
                name=obj.title,
                party=obj.get_party(),
                status=_(u'Active') if obj.is_active else _(u'Inactive'),
            ))

        return results


class Legislature_Members(grok.View):
    grok.context(IFolderish)
    grok.require('zope2.View')
    grok.name('legislature-members')

    def update(self):
        self.legislature = self.request.get('legislature', None)
        if self.legislature is not None:
            catalog = api.portal.get_tool('reference_catalog')
            self.legislature = catalog.lookupObject(self.legislature)

    def get_legislature_members(self):
        """Return dictionary with two lists of members of the legislature
        specified in the variable passed on the request. The 'active' key
        includes all members in the active state; the 'inactive' key includes
        all members in the inactive state.
        """
        if self.legislature is not None:
            members = self.legislature.get_legislature_members()
            by_status = {}
            by_status['active'] = [i for i in members if i.is_active]
            by_status['inactive'] = [i for i in members if not i.is_active]
            return by_status


class Legislatures(grok.View):
    """Return list of legislatures as <options> of a <select>. If present, the
    current legislature is selected.
    """
    grok.context(IFolderish)
    grok.require('zope2.View')

    OPTION_SELECTED = u'<option value="{0}" selected>{1}</option>'
    OPTION = u'<option value="{0}">{1}</option>'

    def render(self):
        legislatures = _get_legislatures()
        options = []
        for item in legislatures:
            if item.is_current:
                options.append(
                    self.OPTION_SELECTED.format(item.UID(), item.long_title))
            else:
                options.append(
                    self.OPTION.format(item.UID(), item.long_title))

        return u'\n'.join(options)
