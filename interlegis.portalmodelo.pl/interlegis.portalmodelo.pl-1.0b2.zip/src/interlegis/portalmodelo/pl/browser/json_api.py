# -*- coding: utf-8 -*-
from five import grok
from interlegis.portalmodelo.api.utils import type_cast
from interlegis.portalmodelo.pl.interfaces import ILegislature
from interlegis.portalmodelo.pl.interfaces import IParliamentarian
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import getUtility
from zope.schema import getFieldsInOrder

import json


class JSONView(grok.View):
    """Generates a JSON with information about parliamentarians and
    legislatures on site.
    """
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')
    grok.name('pl-json')

    def render(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        j = {}
        j['parliamentarians'] = self.get_parliamentarians()
        j['legislatures'] = self.get_legislatures()
        return json.dumps(j, sort_keys=True, indent=4)

    def update(self):
        self.catalog = api.portal.get_tool('portal_catalog')

    def serialize(self, results):
        """Serialize fields of a list of Dexterity-based content type objects.

        :param results: [required] list of objects to be serialized
        :type results: list of catalog brains
        :returns: list of serialized objects
        :rtype: list of dictionaries
        """
        s = []
        for i in results:
            obj = i.getObject()
            # find out object schema to list its fields
            schema = getUtility(IDexterityFTI, name=obj.portal_type).lookupSchema()
            # initialize a dictionary with the object uri
            # XXX: should we use the UUID?
            fields = dict(uri=obj.absolute_url())
            # continue with the rest of the fields
            for name, field in getFieldsInOrder(schema):
                # 'name' could be a @property and not a real field
                if not hasattr(obj, name):
                    continue
                value = getattr(obj, name)
                fields[name] = type_cast(value, obj=obj)
            s.append(fields)
        return s

    def get_legislatures(self):
        """Return list of Legislature objects on site as a list of
        dictionaries.
        """
        results = self.catalog(object_provides=ILegislature.__identifier__)
        return self.serialize(results)

    def get_parliamentarians(self):
        """Return list of Parliamentarian objects on site as a list of
        dictionaries.
        """
        results = self.catalog(object_provides=IParliamentarian.__identifier__)
        return self.serialize(results)
