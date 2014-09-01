# -*- coding: utf-8 -*-

from collective.recaptcha.settings import IRecaptchaSettings
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry
from plone.testing import z2
from zope.component import getUtility
from zope.configuration import xmlconfig


class ContactAuthorLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import collective.contactauthor
        import collective.recaptcha
        xmlconfig.file('configure.zcml',
                       collective.contactauthor,
                       context=configurationContext)
        z2.installProduct(app, 'collective.contactauthor')
        z2.installProduct(app, 'collective.recaptcha')

    def setUpPloneSite(self, portal):
        portal.portal_properties.site_properties.allowAnonymousViewAbout = True
        portal.MailHost.manage_makeChanges(title="The mail host", smtp_host='localhost', smtp_port=25)
        portal.manage_changeProperties(email_from_address='sysadmi@asdf.com', email_from_name='Root')
        applyProfile(portal, 'collective.contactauthor:default')
        #quickInstallProduct(portal, 'collective.contactauthor')
        setRoles(portal, TEST_USER_ID, ['Member', 'Manager'])
        acl_users = portal.acl_users
        acl_users.userFolderAddUser('user1', 'secret', ['Member'], [])
        member = portal.portal_membership.getMemberById('user1') 
        member.setMemberProperties({"email": 'user1@asdf.com'})
        acl_users.userFolderAddUser('user2', 'secret', ['Member'], [])
        member = portal.portal_membership.getMemberById('user2') 
        member.setMemberProperties({"email": 'user2@asdf.com'})
        acl_users.userFolderAddUser('user3', 'secret', ['Member'], [])
        # recaptcha
        registry = getUtility(IRegistry)
        registry.registerInterface(IRecaptchaSettings)
        recaptcha_settings = registry.forInterface(IRecaptchaSettings)
        recaptcha_settings.public_key = u'111'
        recaptcha_settings.private_key = u'222'


CONTACT_AUTHOR_FIXTURE = ContactAuthorLayer()
CONTACT_AUTHOR_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(CONTACT_AUTHOR_FIXTURE, ),
                       name="ContactAuthor:Integration")
CONTACT_AUTHOR_FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(CONTACT_AUTHOR_FIXTURE, ),
                       name="ContactAuthor:Functional")

