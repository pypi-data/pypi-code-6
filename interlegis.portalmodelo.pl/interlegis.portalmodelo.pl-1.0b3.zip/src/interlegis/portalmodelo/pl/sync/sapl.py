# -*- coding: utf-8 -*-
from five import grok
from interlegis.portalmodelo.pl.config import PROJECTNAME
from interlegis.portalmodelo.pl.sync import utils
from interlegis.portalmodelo.pl.sync.controlpanel import ISyncSettings
from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFCore.interfaces import ISiteRoot
from z3c.relationfield import RelationValue
from zope.intid.interfaces import IIntIds
from zope.component import getUtility

import json
import logging


log = logging.getLogger(PROJECTNAME)


class SyncSAPL(grok.View):
    grok.context(ISiteRoot)
    grok.name('sync-sapl')
    grok.require('cmf.ManagePortal')

    path = ''
    remote = ''

    def __init__(self, context, request):
        super(SyncSAPL, self).__init__(context, request)
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISyncSettings)
        self.path = settings.path
        self.remote = settings.remote

    def render(self, *args, **kwargs):
        """ Sync content
        """
        counter = self.create_content()
        return 'Synced %d legislatures' % (counter['legislatures'])

    def get_base_folder(self):
        """ Get the base folder for legislative process content
        """
        base_folder = api.content.get(self.path)
        return base_folder

    def get_parliamentarians_folder(self):
        """ Get the base folder for legislative process content
        """
        base_folder = self.get_base_folder()
        return base_folder['parlamentares']

    def get_legislatures_folder(self):
        """Return the folder on which legislatures must be created.
        """
        base_folder = self.get_base_folder()
        return base_folder['legislaturas']

    def get_data(self):
        """ Access SAPL server get JSON data and convert it to
            Python format
        """
        data, content_type = utils.get_remote_data(self.remote)
        if not data:
            data = '{}'

        try:
            data = json.loads(data)
        except ValueError:
            log.info('Wrong response from backend')
            data = {}
        return data

    def create_content(self):
        """ Create content
        """
        counter = {
            'legislatures': 0,
            'parliamentarians': 0,
        }
        if not (self.path and self.remote):
            return counter
        parliamentarians_folder = self.get_parliamentarians_folder()
        data = self.get_data()
        # Create parliamentarians
        parliamentarians = data.get('parliamentarians', [])
        for par in parliamentarians:
            par = utils.adjust_types(par)
            # XXX: we want to store parliamentarian in the 'parlamentares'
            #      folder; for now we just hardcode it
            o = self.get_parliamentarian(parliamentarians_folder, par)
            self.update_parliamentarian(o, par)
            counter['parliamentarians'] += 1

        # Create legislatures
        legislatures_folder = self.get_legislatures_folder()
        legislatures = data.get('legislatures', [])
        for leg in legislatures:
            leg = utils.adjust_types(leg)
            o = self.get_legislature(legislatures_folder, leg)
            self.update_legislature(o, leg)
            counter['legislatures'] += 1
        return counter

    # TODO: Memoize
    def all_parliamentarians(self):
        folder = self.get_parliamentarians_folder()
        parliamentarians = {}
        intids = getUtility(IIntIds)
        for obj in folder.objectValues():
            if not obj.portal_type == 'Parliamentarian':
                continue
            parliamentarians[obj.getId()] = intids.getId(obj)
        return parliamentarians

    def get_parliamentarian(self, folder, parliamentarian):
        """Get a Parlamentarian object within the specified folder.
        If an object does not exists create it based on the information provided
        inside the folder specified and just return the object.

        :param folder: [required] context on which we will create the object.
        :type context: context object
        :param parliamentarian: [required] information of the parliamentarian.
        :type context: dictionary
        :returns: Parliamentarian object
        :rtype: Parliamentarian content type
        """
        oId = parliamentarian.get('id')
        title = parliamentarian.get('title')
        if oId not in folder.objectIds():
            o = api.content.create(
                folder, type='Parliamentarian', id=oId, title=title)
        else:
            o = folder[oId]
        return o

    def update_parliamentarian(self, o, parliamentarian):
        o.title = parliamentarian.get('title')
        o.full_name = parliamentarian.get('full_name')
        o.description = parliamentarian.get('description')
        o.birthday = parliamentarian.get('birthday')
        o.address = parliamentarian.get('address')
        o.postal_code = parliamentarian.get('postal_code')
        o.telephone = parliamentarian.get('telephone')
        # Image
        image = parliamentarian.get('image')
        if image:
            o.image = image
        party_affiliation = parliamentarian.get('party_affiliation')
        # Party affiliation
        for affiliation in party_affiliation:
            affiliation = utils.adjust_types(affiliation)
        o.party_affiliation = party_affiliation
        log.info('Parlamentarian %s updated' % o.Title())

    def get_legislature(self, folder, legislature):
        oId = legislature.get('id')
        title = legislature.get('title')
        if oId not in folder.objectIds():
            o = api.content.create(
                folder, type='Legislature', id=oId, title=title)
        else:
            o = folder[oId]
        return o

    def update_legislature(self, o, legislature):
        parliamentarians = self.all_parliamentarians()
        o.title = legislature.get('title')
        o.description = legislature.get('description')
        o.start_date = legislature.get('start_date')
        o.end_date = legislature.get('end_date')
        members = []
        members_ids = legislature.get('members', [])
        for mId in members_ids:
            if mId not in parliamentarians:
                continue
            members.append(RelationValue(parliamentarians[mId]))
        o.members = members
        sessions = legislature.get('sessions', [])
        for session in sessions:
            session = utils.adjust_types(session)
            oSession = self.get_session(o, session)
            self.update_session(oSession, session)

        log.info('Legislature %s updated' % o.Title())

    def get_session(self, legislature, session):
        oId = session.get('id')
        title = session.get('title')
        if oId not in legislature.objectIds():
            o = api.content.create(
                legislature, type='Session', id=oId, title=title)
        else:
            o = legislature[oId]
        return o

    def update_session(self, o, session):
        o.title = session.get('title')
        o.description = session.get('description')
        o.start_date = session.get('start_date')
        o.end_date = session.get('end_date')
        legislative_board = session.get('legislative_board', [])
        o.legislative_board = legislative_board
        log.info('Session %s updated' % o.Title())
