# -*- coding: utf-8 -*-

from datetime import datetime
from five import grok
from interlegis.portalmodelo.pl import _
from interlegis.portalmodelo.pl.interfaces import ILegislature
from plone.dexterity.content import Container


class Legislature(Container):
    """Represent a legislature."""
    grok.implements(ILegislature)

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
        """Return a string formed by the number of the legislature and the
        years. If the legislature is the current one, it also displays this
        information.
        """
        title, start, end = self.title, self.start_date.year, self.end_date.year
        # FIXME: the translation is not being applied
        # infix = _(u'legislature_infix_long_title', default=u' Legislature')
        infix = ''
        long_title = u'{0}{1} ({2} - {3})'.format(title, infix, start, end)
        if self.is_current:
            # XXX: can't put this translation to work
            # long_title += u' ({0})'.format(_(u'Current'))
            long_title += u' ({0})'.format(_(u'Atual'))

        return long_title

    def get_legislature_members(self):
        """Return list of parliamentarians on the legislature.
        """
        return [i.to_object for i in self.members]
