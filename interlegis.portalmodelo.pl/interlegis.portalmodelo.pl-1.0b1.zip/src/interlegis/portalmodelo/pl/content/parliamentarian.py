# -*- coding: utf-8 -*-

from five import grok
from interlegis.portalmodelo.pl.interfaces import IParliamentarian
from plone.dexterity.content import Item
from zc.relation.interfaces import ICatalog
from zope.intid.interfaces import IIntIds
from zope.component import getUtility


class Parliamentarian(Item):
    """Represent a parliamentarian."""
    grok.implements(IParliamentarian)

    def get_party(self):
        """Return current party afiliation, which is the one that has no date
        of disaffiliation.
        """
        for affiliation in self.party_affiliation:
            if affiliation['date_disaffiliation'] is None:
                return affiliation['party']

    def get_legislatures(self):
        """Return list of legislatures on which the parliamentarian was
        elected to serve.
        """
        intids = getUtility(IIntIds)
        catalog = getUtility(ICatalog)
        # search all legislatures that have this parliamentarian as member
        legislatures = catalog.findRelations({'to_id': intids.getId(self)})
        # if current one is listed, then the parliamentarian is active
        return [r.from_object for r in legislatures]

    @property
    def is_active(self):
        """Return True if parliamentarian is member of current legislature.
        """
        current = [r for r in self.get_legislatures() if r.is_current]
        return current != []
