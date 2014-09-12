# -*- coding: utf-8 -*-
from urlparse import urlparse

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, Client

from mailto import mailto
from mailto.models import UserOptin, Mail


class OptinCreationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.client = Client()

    def test_has_optin(self):
        self.assertIsInstance(self.user.optin, UserOptin)
        self.assertTrue(self.user.optin.optin)


class MailtoNewMailTest(TestCase):

    def test_mailto_with_new_mail(self):
        mailto(['test@localhost'], 'test')

        email = Mail.objects.get(slug='test', language_code=settings.LANGUAGE_CODE)

        self.assertIsNotNone(email)

        self.assertFalse(email.active)
        self.assertEqual(email.slug, 'test')
        self.assertEqual(email.language_code, settings.LANGUAGE_CODE)
        self.assertIsNotNone(email.template)

        self.assertIsNotNone(email.sender_email)
        self.assertIsNone(email.sender_name)
        self.assertIsNone(email.reply_to)
        self.assertIsNone(email.cc)
        self.assertIsNone(email.bcc)

        self.assertEqual(email.subject, 'test')
        self.assertEqual(email.plain, 'test')
        self.assertIsNone(email.html)

        self.assertTrue(email.optout)

    def test_malto_with_new_mail_not_sent(self):
        self.assertEqual(len(mail.outbox), 0)


class MailtoTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', email='test@localhost')
        mailto(['test@localhost'], 'test')
        self.mail = Mail.objects.get(slug='test', language_code=settings.LANGUAGE_CODE)

    def test_send_inactive(self):
        self.mail.active = False
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 0)

    def test_send_active(self):
        self.mail.active = True
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(mail.outbox[0].body, 'test')
        self.assertEqual(mail.outbox[0].to, ['test@localhost'])
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].cc, [])
        self.assertEqual(mail.outbox[0].bcc, [])
        self.assertEqual(mail.outbox[0].alternatives, [])
        self.assertEqual(mail.outbox[0].extra_headers, {})

    def test_send_active_with_optin(self):
        self.mail.active = True
        self.mail.save()

        self.user.optin.optin = True
        self.user.optin.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 1)

    def test_send_inactive_with_optin(self):
        self.mail.active = False
        self.mail.save()

        self.user.optin.optin = True
        self.user.optin.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 0)

    def test_send_active_with_optout(self):
        self.mail.active = True
        self.mail.save()

        self.user.optin.optin = False
        self.user.optin.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 0)

    def test_send_cc_recipients(self):
        self.mail.active = True
        self.mail.cc = 'cc1@localhost, cc2@localhost,cc3@localhost'
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(mail.outbox[0].body, 'test')
        self.assertEqual(mail.outbox[0].to, ['test@localhost'])
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].cc, ['cc1@localhost', 'cc2@localhost', 'cc3@localhost'])
        self.assertEqual(mail.outbox[0].bcc, [])
        self.assertEqual(mail.outbox[0].alternatives, [])
        self.assertEqual(mail.outbox[0].extra_headers, {})

    def test_send_bcc_recipients(self):
        self.mail.active = True
        self.mail.bcc = 'bcc1@localhost, bcc2@localhost,bcc3@localhost'
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(mail.outbox[0].body, 'test')
        self.assertEqual(mail.outbox[0].to, ['test@localhost'])
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].cc, [])
        self.assertEqual(mail.outbox[0].bcc, ['bcc1@localhost', 'bcc2@localhost', 'bcc3@localhost'])
        self.assertEqual(mail.outbox[0].alternatives, [])
        self.assertEqual(mail.outbox[0].extra_headers, {})

    def test_send_reply_to(self):
        self.mail.active = True
        self.mail.reply_to = 'noreply@localhost'
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(mail.outbox[0].body, 'test')
        self.assertEqual(mail.outbox[0].to, ['test@localhost'])
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].cc, [])
        self.assertEqual(mail.outbox[0].bcc, [])
        self.assertEqual(mail.outbox[0].alternatives, [])
        self.assertEqual(mail.outbox[0].extra_headers, {
            'Reply-To': 'noreply@localhost'
        })

    def test_send_email_address_with_name(self):
        self.mail.active = True
        self.mail.sender_name = 'John Doe'
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(mail.outbox[0].body, 'test')
        self.assertEqual(mail.outbox[0].to, ['test@localhost'])
        self.assertEqual(mail.outbox[0].from_email, '%s <%s>' % ('John Doe', settings.DEFAULT_FROM_EMAIL))
        self.assertEqual(mail.outbox[0].cc, [])
        self.assertEqual(mail.outbox[0].bcc, [])
        self.assertEqual(mail.outbox[0].alternatives, [])
        self.assertEqual(mail.outbox[0].extra_headers, {})

    def test_send_email_with_kwargs(self):
        self.mail.active = True
        self.mail.reply_to = 'noreply@localhost'
        self.mail.cc = 'cc@localhost'
        self.mail.bcc = 'bcc@localhost'
        self.mail.save()

        mailto(['test@localhot'], 'test', **{
            'from_email': 'from@localhost',
            'cc': ['cc1@localhost', 'cc2@localhost'],
            'bcc': ['bcc1@localhost', 'bcc2@localhost'],
            'reply_to': 'reply-to@localhost',
            'headers': {
                'header1': 'header_value_1',
            },
            'attachments': [('mail.js', '/static/js/mail.js', 'text/javascript')]
        })

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, 'from@localhost')
        self.assertEqual(mail.outbox[0].cc, ['cc@localhost', 'cc1@localhost', 'cc2@localhost'])
        self.assertEqual(mail.outbox[0].bcc, ['bcc@localhost', 'bcc1@localhost', 'bcc2@localhost'])
        self.assertEqual(mail.outbox[0].extra_headers.get('header1'), 'header_value_1')
        self.assertEqual(mail.outbox[0].extra_headers.get('Reply-To'), 'reply-to@localhost')
        self.assertEqual(mail.outbox[0].attachments, [('mail.js', '/static/js/mail.js', 'text/javascript')])