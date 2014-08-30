# -*- coding: utf-8 -*-

from datetime import date
from interlegis.portalmodelo.pl.sync import utils
from interlegis.portalmodelo.pl.sync.controlpanel import ISyncSettings
from interlegis.portalmodelo.pl.testing import INTEGRATION_TESTING
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import json
import os
import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        path = os.path.join(os.path.dirname(__file__))
        # Image file should be available to urllib2 working dir
        fh = open('erico-verissimo.jpg', 'wb')
        fh.write(open(os.path.join(path, 'erico-verissimo.jpg')).read())
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISyncSettings)
        self.remote = 'file://' + os.path.join(path, 'sapl.json')
        self.settings.path = u'/processo-legislativo'
        self.settings.remote = unicode(self.remote)
        self.folder = self.portal['processo-legislativo']
        # this is hardcoded right now
        self.parliamentarians = self.folder['parlamentares']
        self.legislatures = self.folder['legislaturas']
        self.view = api.content.get_view(
            name='sync-sapl', context=self.portal, request=self.request)

    def test_adjust_types(self):
        json_data = """{"description": "","end_date": "2016-12-31", "id": "legislature-01",
            "members": ["000000000001"], "start_date": "2013-01-01", "title": "1st Legislature"}
        """
        data = utils.adjust_types(json.loads(json_data))
        self.assertEqual(data['end_date'], date(2016, 12, 31))
        self.assertEqual(data['start_date'], date(2013, 1, 1))

    def test_view(self):
        view = self.view
        self.assertTrue(view)

    def test_view_sync(self):
        view = self.view
        # folder was create at installarion so a normal user doesn't
        # have permissions to add objects to it
        with api.env.adopt_roles(['Manager']):
            counter = view.create_content()
        self.assertEqual(counter['legislatures'], 1)
        self.assertEqual(counter['parliamentarians'], 2)

    def test_view_sync_bad_remote_address(self):
        self.settings.remote = unicode('file' + os.path.join(
            os.path.dirname(__file__), 'sapl_errored.json'
        ))
        view = api.content.get_view(
            name='sync-sapl', context=self.portal, request=self.request)
        counter = view.create_content()
        self.assertEqual(counter['legislatures'], 0)
        self.assertEqual(counter['parliamentarians'], 0)

    def test_view_sync_malformed_json(self):
        self.settings.remote = unicode('file://' + os.path.join(
            os.path.dirname(__file__), 'sapl_errored.json'
        ))
        view = api.content.get_view(
            name='sync-sapl', context=self.portal, request=self.request)
        counter = view.create_content()
        self.assertEqual(counter['legislatures'], 0)

    def test_view_parliamentarians(self):
        view = self.view
        # folder was create at installarion so a normal user doesn't
        # have permissions to add objects to it
        with api.env.adopt_roles(['Manager']):
            counter = view.create_content()
        self.assertEqual(counter['parliamentarians'], 2)
        # Test if content was created
        self.assertIn('000000000001', self.parliamentarians.objectIds())
        self.assertIn('000000000002', self.parliamentarians.objectIds())
        # Test Content Titles
        o = self.parliamentarians['000000000001']
        self.assertEqual(o.Title(), 'Machado de Assis')
        o = self.parliamentarians['000000000002']
        self.assertEqual(o.Title(), 'Erico Verissimo')

    def test_view_parliamentarians_party_affiliation(self):
        view = self.view
        # folder was create at installarion so a normal user doesn't
        # have permissions to add objects to it
        with api.env.adopt_roles(['Manager']):
            view.create_content()
        # Test Machado de Assis party affiliation
        o = self.parliamentarians['000000000001']
        party_affiliation = o.party_affiliation
        self.assertEqual(len(party_affiliation), 1)
        self.assertEqual(party_affiliation[0]['party'], 'ABL')
        self.assertEqual(
            party_affiliation[0]['date_affiliation'],
            date(1975, 12, 19)
        )
        # Test Erico Verissimo party affiliation
        o = self.parliamentarians['000000000002']
        party_affiliation = o.party_affiliation
        self.assertEqual(len(party_affiliation), 2)
        self.assertEqual(party_affiliation[0]['party'], 'ABL')
        self.assertEqual(party_affiliation[1]['party'], 'GAU')
        self.assertEqual(
            party_affiliation[0]['date_disaffiliation'],
            date(1975, 11, 28)
        )
        self.assertIsNone(party_affiliation[1]['date_disaffiliation'])

    def test_view_parliamentarians_image(self):
        from plone.namedfile.file import NamedBlobImage
        view = self.view
        # folder was create at installarion so a normal user doesn't
        # have permissions to add objects to it
        with api.env.adopt_roles(['Manager']):
            view.create_content()
        # Machado de Assi image is empty
        o = self.parliamentarians['000000000001']
        self.assertIsNone(o.image)
        # dummy image must be present on output
        view = api.content.get_view(name='view', context=o, request=self.request)
        self.assertIn('dummy.png', view())

        # Erico Verissimo image is not empty
        o = self.parliamentarians['000000000002']
        self.assertIsInstance(o.image, NamedBlobImage)
        # dummy image must not be present on output
        view = api.content.get_view(name='view', context=o, request=self.request)
        self.assertNotIn('dummy.png', view())

    def test_view_legislatures(self):
        view = self.view
        # folder was create at installarion so a normal user doesn't
        # have permissions to add objects to it
        with api.env.adopt_roles(['Manager']):
            counter = view.create_content()
        self.assertEqual(counter['legislatures'], 1)
        # Test if content was created
        self.assertIn('legislature-01', self.legislatures.objectIds())
        # Test if content was created
        o = self.legislatures['legislature-01']
        self.assertEqual(o.Title(), '1st Legislature')
        # Test if dates are correct
        self.assertEqual(o.start_date, date(2013, 1, 1))
        self.assertEqual(o.end_date, date(2016, 12, 31))

    def test_view_legislatures_members(self):
        view = self.view
        # folder was create at installarion so a normal user doesn't
        # have permissions to add objects to it
        with api.env.adopt_roles(['Manager']):
            view.create_content()

        o = self.legislatures['legislature-01']
        members = o.members
        self.assertEqual(len(members), 2)
        # Get one member
        parliamentarian = self.parliamentarians['000000000001']
        # Should be the same
        self.assertEqual(members[0].to_object, parliamentarian)

        # Get the other member
        parliamentarian = self.parliamentarians['000000000002']
        # Should be the same
        self.assertEqual(members[1].to_object, parliamentarian)

    def test_view_legislatures_sessions(self):
        view = self.view
        # folder was create at installarion so a normal user doesn't
        # have permissions to add objects to it
        with api.env.adopt_roles(['Manager']):
            view.create_content()

        o = self.legislatures['legislature-01']
        sessions = o.objectValues()
        self.assertEqual(len(sessions), 2)
        # Validate session datas
        session = sessions[0]
        self.assertEqual(session.Title(), '1st (2013-2014)')
        self.assertEqual(len(session.legislative_board), 1)

        session = sessions[1]
        self.assertEqual(session.Title(), '2nd (2015-2016)')
        self.assertEqual(len(session.legislative_board), 2)
