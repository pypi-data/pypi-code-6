# -*- coding: utf-8 -*-

from five import grok
from interlegis.portalmodelo.pl.interfaces import ISession
from plone import api
from plone.directives import dexterity
from plone.memoize import view
from Products.CMFCore.interfaces import IFolderish

grok.templatedir('templates')


class Session_View(dexterity.DisplayForm):
    grok.context(ISession)
    grok.require('zope2.View')
    grok.name('view')

    @view.memoize
    def board_members(self):
        """Return list of members of the legislature board.
        """
        catalog = api.portal.get_tool('portal_catalog')
        results = []
        for member in self.context.legislative_board:
            # as we are not storing a relation, we have only the title
            # of the object and not the object; let's search for it
            name, position = member['member'], member['position']
            brains = catalog(Title=name)
            # we should have only one result if the name is right, in
            # any other case we should not return additional information
            if len(brains) == 1:
                obj = brains[0].getObject()
                results.append(dict(
                    full_name=obj.full_name,
                    url=obj.absolute_url(),
                    name=obj.title,
                    party=obj.get_party(),
                    position=position,
                ))
            else:
                results.append(dict(
                    full_name=u'',
                    url=u'',
                    name=name,
                    party=u'',
                    position=position,
                ))

        return results


class Legislative_Board(grok.View):
    grok.context(IFolderish)
    grok.require('zope2.View')
    grok.name('mesa-diretora')


class Board_Members(grok.View):
    grok.context(IFolderish)
    grok.require('zope2.View')
    grok.name('board-members')

    def update(self):
        self.session = self.request.get('session', None)
        if self.session is not None:
            catalog = api.portal.get_tool('reference_catalog')
            self.session = catalog.lookupObject(self.session)

    def get_legislative_board_members(self):
        """Return list of board members of the legislative session specified
        in the variable passed on the request.
        """
        if self.session is not None:
            return self.session.get_legislative_board_members()

    def get_position(self, member):
        """Return position of member of the board.
        """
        if self.session is not None:
            return self.session.get_position(member)


class Sessions(grok.View):
    """Return list of sessions as <options> of a <select>. If present, the
    current session is selected.
    """
    grok.context(IFolderish)
    grok.require('zope2.View')

    OPTION_SELECTED = u'<option value="{0}" selected>{1}</option>'
    OPTION = u'<option value="{0}">{1}</option>'

    def render(self):
        legislature = self.request.get('legislature', None)
        if legislature is None:
            return None

        catalog = api.portal.get_tool('reference_catalog')
        legislature = catalog.lookupObject(legislature)

        if legislature is None:
            return None

        sessions = legislature.getFolderContents()

        if not sessions:
            return None

        sessions = [i.getObject() for i in sessions]
        sessions = sorted(sessions, key=lambda l: l.start_date)
        options = []
        for item in sessions:
            if item.is_current:
                options.append(
                    self.OPTION_SELECTED.format(item.UID(), item.long_title))
            else:
                options.append(
                    self.OPTION.format(item.UID(), item.long_title))

        return u'\n'.join(options)
