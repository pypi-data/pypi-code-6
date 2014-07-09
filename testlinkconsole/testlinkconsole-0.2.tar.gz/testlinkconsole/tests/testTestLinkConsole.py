import unittest
import mock
import mox
import sys
import ConfigParser
import logging

from StringIO import StringIO
#from testlinkclient import TestlinkClient
from testlinkconsole import TestLinkConsole

class TestTestLinkConsole(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger('logger')
        self.testlinkconsole = TestLinkConsole(ConfigParser.RawConfigParser(), logger)

    def test_do_plugins(self):
        self.assertEquals(self.testlinkconsole.do_plugins('line'),None)

    # LIST
    @unittest.skip('Refactoring')
    def test_do_list_project(self):
        self.assertEquals(self.testlinkconsole.do_list('projects'),None)

    @unittest.skip('Refactoring')
    def test_do_list_campagnes(self):
        self.assertEquals(self.testlinkconsole.do_list('campagnes'), None)

    @unittest.skip('Refactoring')
    def test_do_list_toto(self):
        self.assertEquals(self.testlinkconsole.do_list('toto'), None)
       
    @unittest.skip('Refactoring')
    def test_complete_list(self):
        self.assertItemsEqual(self.testlinkconsole.complete_list('','line','ids','idx'),['projets','campagnes','tests'])
        self.assertEquals(self.testlinkconsole.complete_list('pro','line','ids','idx'),['projets',])

    @mock.patch('__builtin__.print')
    def  test_help_list(self, mock_print):
        sav_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        mock_print.assert_has_call([])
        self.assertEquals(self.testlinkconsole.help_list(),None)
        output = out.getvalue().strip()
        self.assertEquals(output, 'list [content]\n list content from testlink')

    # RUN
    @unittest.skip('Refactoring')
    def test_run(self):
        self.assertEquals(self.testlinkconsole.do_run('line'), None)

    @mock.patch('__builtin__.print')
    def  test_help_run(self, mock_print):
        sav_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        mock_print.assert_has_call([])
        self.assertEquals(self.testlinkconsole.help_run(),None)
        output = out.getvalue().strip()
        self.assertEquals(output, 'run\n  run campagne')

