from django.core import mail
from django.core.exceptions import ValidationError
from django.test import TestCase

from emailer.models import ConnectionProfile, EmailTemplate


class EmailTransportTestCase(TestCase):
    fixtures = ['email_templates']

    def test_connection(self):
        # wrong everything
        conn = ConnectionProfile(
            host='such.an.unknown.n0n3Xizt3ht-server.com',
            port=587, use_tls=False,
            username='foobar', password='123')
        self.assertRaises(ValidationError, lambda: conn.clean())

        # valid server, bad credentials
        conn.__dict__.update(host='smtp.gmail.com', use_tls=True)
        self.assertRaises(ValidationError, lambda: conn.clean())

        # TODO: test a valid connection with a dummy server

    def test_email_send(self):
        to = 'user@server.com'

        # render and send the email from a template
        email = EmailTemplate.get('TEST_EMAIL').render(
            to=to, context={'sender': 'Foo', 'destiny': 'Bar'})
        email.send()

        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]

        # make sure we're using the right connection
        connection_profile = ConnectionProfile.objects.all()[0]
        for field in ('host', 'port', 'use_tls', 'username', 'password',):
            self.assertEqual(
                getattr(connection_profile, field),
                getattr(sent_email.connection, field))

        # test email content
        self.assertEqual(set(sent_email.to), set([to]))
        self.assertIn('Bar', sent_email.subject)
        self.assertIn('Foo', sent_email.body)
