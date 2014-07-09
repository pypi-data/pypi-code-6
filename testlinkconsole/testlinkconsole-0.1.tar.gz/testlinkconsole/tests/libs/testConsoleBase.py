#import unittest2 as unittest
import unittest
import mock
import sys
from mock import call
from StringIO import StringIO
import ConfigParser

from libs.consoleBase import ConsoleBase

class TestconsoleBase(unittest.TestCase):

    def setUp(self):
        sav_stdout = sys.stdout
        self.out = StringIO()
        sys.stdout = self.out
        self.consoleBase = ConsoleBase(ConfigParser.RawConfigParser())

    def test_read_config(self):
        self.consoleBase.LIST_VARIABLE={'commande': 'Un commande',}
        self.assertEquals(self.consoleBase.read_config(), None)


    # CONFIG
    @mock.patch('__builtin__.print')
    def test_help_config(self, mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.consoleBase.help_config(),None)
        output = self.out.getvalue().strip()
        self.assertEquals(output, 'config\nshow configuration')
   
    @mock.patch('__builtin__.print')
    def test_do_config(self,mock_print):
        mock_print.assert_has_calls([])
        self.consoleBase.LIST_VARIABLE={'commande': 'Un commande',}
        self.consoleBase.commande='test'
        self.assertEquals(self.consoleBase.do_config('line'),None)
   
    # SAVE
    @mock.patch('__builtin__.open')
    def test_do_save(self, mock_open):
        configuration = ConfigParser.RawConfigParser()
        configuration.add_section('console')
        self.consoleBase.LIST_VARIABLE={'commande' : 'une commande',}
        self.consoleBase.commande='test'
        self.consoleBase.config=configuration
        mock_open.assert_has_calls([])
        self.assertEquals(self.consoleBase.do_save('line'),None)

    @mock.patch('__builtin__.print')
    def test_help_save(self, mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.consoleBase.help_save(),None)

    # GET    
    @mock.patch('__builtin__.print')
    def test_help_get(self,mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.consoleBase.help_get(),None)
    
    @mock.patch('__builtin__.print')
    def test_do_get_variableNotFound(self, mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.consoleBase.do_get('line'),None)

    @mock.patch('__builtin__.print')
    def test_do_get_variable(self, mock_print):
        self.consoleBase.LIST_VARIABLE={'commande' : 'une commande',}
        self.consoleBase.commande='test'
        mock_print.assert_has_calls([])
        self.assertEquals(self.consoleBase.do_get('commande'),None)

    def test_complete_get_notext(self):
        self.consoleBase.LIST_VARIABLE={'commande' : 'une commande',}
        self.assertEquals(self.consoleBase.complete_get('','line','ids','idx'),['commande',])
        self.assertEquals(self.consoleBase.complete_get('com','line','ids','idx'),['commande',])

    def test_complete_get_cmd(self):
        self.consoleBase.LIST_VARIABLE={'commande' : 'une commande', 'autre' : 'autre commande',}
        self.assertItemsEqual(self.consoleBase.complete_get('','line','ids','idx'),['commande','autre'])
        self.assertEquals(self.consoleBase.complete_get('com','line','ids','idx'),['commande',])

    # SET
    @mock.patch('__builtin__.print')
    def test_help_set(self, mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.consoleBase.help_set(),None)

    @mock.patch('__builtin__.print')
    def test_do_set(self, mock_print):
        mock_print.assert_has_calls([])
        self.assertEquals(self.consoleBase.do_set('variable value'),None)

    def test_complete_set_notext(self):
        self.consoleBase.LIST_VARIABLE={'commande' : 'une commande',}
        self.assertEquals(self.consoleBase.complete_set('','line','ids','idx'),['commande',])
        self.assertEquals(self.consoleBase.complete_set('com','line','ids','idx'),['commande',])

    def test_complete_set_cmd(self):
        self.consoleBase.LIST_VARIABLE={'commande' : 'une commande', 'autre' : 'autre commande',}
        self.assertItemsEqual(self.consoleBase.complete_set('','line','ids','idx'),['commande','autre'])
        self.assertEquals(self.consoleBase.complete_set('com','line','ids','idx'),['commande',])

if __name__ == '__main__':
    unittest.main()
