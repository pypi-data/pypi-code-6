# -*- coding: utf-8 -*-

from datetime import datetime
from five import grok
from interlegis.portalmodelo.pl import _
from interlegis.portalmodelo.pl.config import PROJECTNAME
from interlegis.portalmodelo.pl.interfaces import IParliamentarian
from interlegis.portalmodelo.pl.interfaces import ISession
from plone import api
from plone.dexterity.content import Item

import logging

logger = logging.getLogger(PROJECTNAME)


class Session(Item):
    """Represent a legislative session."""
    grok.implements(ISession)

    @property
    def is_current(self):
        """Return True if current date is between start_date and end_date.
        """
        # start_date and end_date type is datetime.date
        # we need to convert current date to datetime.date
        now = datetime.now().date()
        return now >= self.start_date and now <= self.end_date

    @property
    def long_title(self):
        """Return a string formed by the number of the session and the
        years. If the legislature is the current one, it also displays this
        information.
        """
        title, start, end = self.title, self.start_date.year, self.end_date.year
        # FIXME: the translation is not being applied
        # infix = _(u'session_infix_long_title', default=u' Legislative Session')
        infix = ''
        long_title = u'{0}{1} ({2} - {3})'.format(title, infix, start, end)
        if self.is_current:
            # XXX: can't put this translation to work
            # long_title += u' ({0})'.format(_(u'Current'))
            long_title += u' ({0})'.format(_(u'Atual'))

        return long_title

    def get_legislative_board_members(self):
        """Return list of parliamentarians on the legislative session board.
        """
        catalog = api.portal.get_tool('portal_catalog')
        interface = IParliamentarian.__identifier__
        members = []

        for i in self.legislative_board:
            # as we are not storing a relation, we have only the title
            # of the object and not the object; let's search for it
            brains = catalog(Title=i['member'], object_provides=interface)
            # we should have only one result if the name is right
            if len(brains) == 1:
                members.append(brains[0].getObject())
            else:
                msg = u'{0}: Invalid parliamentarian name'.format(repr(self))
                logger.info(msg)

        return members

    def get_position(self, member):
        """Return position of member of the board.
        """
        if not IParliamentarian.providedBy(member):
            return None

        for i in self.legislative_board:
            if i['member'] == member.title:
                return i['position']

        return None
