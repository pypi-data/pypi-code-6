# -*- coding: utf-8 -*-

from interlegis.portalmodelo.pl.interfaces import ILegislature
from plone import api


def _get_legislatures():
    """Return all legislatures sorted in reverse order.
    """
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog(object_provides=ILegislature.__identifier__)

    if not results:
        return []

    results = [r.getObject() for r in results]
    results = sorted(results, key=lambda l: l.start_date, reverse=True)
    return results
