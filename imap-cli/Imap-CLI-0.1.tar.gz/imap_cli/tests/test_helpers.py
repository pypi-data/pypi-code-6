# -*- coding: utf-8 -*-


"""Test helpers"""


from imap_cli import config
from imap_cli import helpers
import unittest


class HelpersTest(unittest.TestCase):
    def setUp(self):
        self.ctx = config.new_context_from_file('~/.config/imap-cli')

#    def test_connect(self):
#        helpers.connect(self.ctx)
#        assert getattr(self.ctx, 'mail_account') is not None
#
#    def test_list_dir(self):
#        helpers.connect(self.ctx)
#        self.ctx.mail_account.select()
#        mails = helpers.list_mail(self.ctx)
#        assert isinstance(mails, list)
#
#    def test_disconnect(self):
#        helpers.connect(self.ctx)
#        self.ctx.mail_account.select()
#        helpers.disconnect(self.ctx)
#        assert getattr(self.ctx, 'mail_account').state == 'LOGOUT'
