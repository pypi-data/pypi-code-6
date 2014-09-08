# -*- coding: UTF-8 -*-
from collective.singing.interfaces import IChannel
from collective.singingnotify.mail import ConfirmNotifyAction, ConfirmNotifyAddForm, ConfirmNotifyEditForm
from email.MIMEText import MIMEText
from plone.app.contentrules.rule import Rule
from plone.app.contentrules.tests.base import ContentRulesTestCase
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleAction, IExecutable
from Products.MailHost.interfaces import IMailHost
from Products.SecureMailHost.SecureMailHost import SecureMailHost
from collective.dancing.events import IConfirmSubscriptionEvent
from collective.dancing.subscribe import Subscription
from zope.component import getUtility, getMultiAdapter, getSiteManager
from zope.interface import implements

# basic test structure copied from plone.app.contentrules test_action_mail.py


class DummyEvent(object):
    implements(IConfirmSubscriptionEvent)

    def __init__(self, object):
        self.object = object
        self.subscriber = Subscription(channel=self.object,
                                       collector_data={},
                                       composer_data={'email': u'example@foo.it'},
                                       metadata='',
                                       secret='')


class DummySecureMailHost(SecureMailHost):
    meta_type = 'Dummy secure Mail Host'

    def __init__(self, id):
        self.id = id
        self.sent = []

    def _send(self, mfrom, mto, messageText, debug=False):
        self.sent.append(messageText)


class TestConfirmSubscriptionAction(ContentRulesTestCase):

    def afterSetUp(self):
        self.setRoles(('Manager',))
        self.portal.invokeFactory('Folder', 'target')

    def testRegistered(self):
        element = getUtility(IRuleAction, name='plone.actions.NewsletterConfirmNotify')
        self.assertEquals('plone.actions.NewsletterConfirmNotify', element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(IChannel, element.for_)
        self.assertEquals(IConfirmSubscriptionEvent, element.event)

    def testInvokeAddView(self):
        element = getUtility(IRuleAction, name='plone.actions.NewsletterConfirmNotify')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)
        self.failUnless(isinstance(addview, ConfirmNotifyAddForm))
        addview.createAndAdd(data={'subject': 'My Subject',
                                   'source': 'foo@foomail.com',
                                   'dest_addr': 'foo_dest@foomail.com',
                                   'message': 'Hey, Oh!'})

        e = rule.actions[0]
        self.failUnless(isinstance(e, ConfirmNotifyAction))
        self.assertEquals('My Subject', e.subject)
        self.assertEquals('foo@foomail.com', e.source)
        self.assertEquals('foo_dest@foomail.com', e.dest_addr)
        self.assertEquals('Hey, Oh!', e.message)

    def testInvokeEditView(self):
        element = getUtility(IRuleAction, name='plone.actions.NewsletterConfirmNotify')
        e = ConfirmNotifyAction()
        editview = getMultiAdapter((e, self.folder.REQUEST),
                                   name=element.editview)
        self.failUnless(isinstance(editview, ConfirmNotifyEditForm))

    def testExecute(self):
        self.loginAsPortalOwner()
        sm = getSiteManager(self.portal)
        sm.unregisterUtility(provided=IMailHost)
        dummyMailHost = DummySecureMailHost('dMailhost')
        sm.registerUtility(dummyMailHost, IMailHost)
        e = ConfirmNotifyAction()
        e.source = "foo@foomail.com"
        e.dest_addr = "foo_dest@foomail.com"
        e.message = u"User unsubscribed!"
        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder)), IExecutable)
        ex()
        self.failUnless(isinstance(dummyMailHost.sent[0], MIMEText))
        mailSent = dummyMailHost.sent[0]
        self.assertEqual('text/plain; charset="utf-8"',
                        mailSent.get('Content-Type'))
        self.assertEqual("foo@foomail.com", mailSent.get('From'))
        self.assertEqual("foo_dest@foomail.com", mailSent.get('To'))
        self.assertEqual("User unsubscribed!",
                         mailSent.get_payload(decode=True))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestConfirmSubscriptionAction))
    return suite
