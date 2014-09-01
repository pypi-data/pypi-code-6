# -*- coding: utf-8 -*-

import unittest
from zope import interface
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from plone.app.testing import logout
from plone.app.testing import login
from collective.contactauthor.testing import CONTACT_AUTHOR_INTEGRATION_TESTING
from collective.contactauthor.interfaces import IAuthorViewProtectionSettings
from collective.contactauthor.interfaces import IContactAuthorBrowserLayer


class ContactAuthorTestCase(unittest.TestCase):
    
    layer = CONTACT_AUTHOR_INTEGRATION_TESTING

    def setUp(self):
        # to be removed when p.a.testing will fix https://dev.plone.org/ticket/11673
        request = self.layer['request']
        interface.alsoProvides(request, IContactAuthorBrowserLayer)
        logout()

    def getSettings(self):
        registry = queryUtility(IRegistry)
        return registry.forInterface(IAuthorViewProtectionSettings, check=False)

    def test_anonymous_captcha(self):
        # default config: anon user see the captcha and can send messages
        portal = self.layer['portal']
        request = self.layer['request']        
        request.set('ACTUAL_URL', 'http://nohost/plone/author/user1')
        request.set('traverse_subpath', ['user1'])
        output = portal.author()
        self.assertTrue('<input type="text" id="email" name="email" size="25" />' in output)
        self.assertTrue('Spam protection' in output)

    def test_anonymous_totally_free(self):
        # dangerous config: anon user can send messages with no captcha
        settings = self.getSettings()
        settings.protection_level = u'free-for-all'
        portal = self.layer['portal']
        request = self.layer['request']        
        request.set('ACTUAL_URL', 'http://nohost/plone/author/user1')
        request.set('traverse_subpath', ['user1'])
        output = portal.author()
        self.assertTrue('<input type="text" id="email" name="email" size="25" />' in output)
        self.assertFalse('Spam protection' in output)

    def test_anonymous_never_post(self):
        # no anoynmous access (Plone default)
        settings = self.getSettings()
        settings.protection_level = u'authenticated-only'
        portal = self.layer['portal']
        request = self.layer['request']        
        request.set('ACTUAL_URL', 'http://nohost/plone/author/user1')
        request.set('traverse_subpath', ['user1'])
        output = portal.author()
        self.assertFalse('<input type="text" id="email" name="email" size="25" />' in output)
        self.assertTrue('Log in to send feedback' in output)

    def test_member_post(self):
        # a member can send messages to other members
        portal = self.layer['portal']
        request = self.layer['request']        
        login(portal, 'user2')
        request.set('ACTUAL_URL', 'http://nohost/plone/author/user1')
        request.set('traverse_subpath', ['user1'])
        output = portal.author()        
        self.assertFalse('<input type="text" id="email" name="email" size="25" />' in output)
        self.assertTrue('<input class="context" type="submit" name="form.button.Send" value="Send" />' in output)

    def test_member_cant_post_no_recipient_mail(self):
        # a member can't send messages to members with no email
        portal = self.layer['portal']
        request = self.layer['request']        
        login(portal, 'user2')
        request.set('ACTUAL_URL', 'http://nohost/plone/author/user3')
        request.set('traverse_subpath', ['user3'])
        output = portal.author()        
        self.assertFalse('<input type="text" id="email" name="email" size="25" />' in output)
        self.assertFalse('<input class="context" type="submit" name="form.button.Send" value="Send" />' in output)

    def test_member_can_post_no_sender_mail(self):
        # a member can send messages if he haven't any address, but he must provide one
        portal = self.layer['portal']
        request = self.layer['request']        
        login(portal, 'user3')
        request.set('ACTUAL_URL', 'http://nohost/plone/author/user1')
        request.set('traverse_subpath', ['user1'])
        output = portal.author()        
        self.assertTrue('<input type="text" id="email" name="email" size="25" />' in output)
        self.assertTrue('<input class="context" type="submit" name="form.button.Send" value="Send" />' in output)
