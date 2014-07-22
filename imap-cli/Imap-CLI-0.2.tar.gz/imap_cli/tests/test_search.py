# -*- coding: utf-8 -*-


"""Test helpers"""


import imaplib
import unittest

import mock

from imap_cli import config


class HelpersTest(unittest.TestCase):
    def setUp(self):
        self.ctx = config.new_context_from_file('~/.config/imap-cli')

        imaplib.IMAP4_SSL = mock.Mock()
        imap_connection = imaplib.IMAP4_SSL('localhost')
        imap_connection.fetch = mock.Mock(return_value=('OK', [('1 (RFC822 {2323}', "EMAIL CONTENT"), ')']))
        imap_connection.list = mock.Mock(
            return_value=('OK', ['(\\HasNoChildren) "." "Directory_name"', '(\\HasNoChildren) "." "INBOX"'])
        )
        imap_connection.login = mock.Mock(return_value=('OK', ['Logged in']))
        imap_connection.select = mock.Mock(return_value=('OK', ['1']))
        imap_connection.status(return_value=('OK', ['"Directory_name" (MESSAGES 1 RECENT 1 UNSEEN 0)']))

    def test_before(self):
        pass

    def test_after(self):
        pass

    def test_full_text(self):
        pass

    def test_from(self):
        pass

    def test_tags(self):
        pass
