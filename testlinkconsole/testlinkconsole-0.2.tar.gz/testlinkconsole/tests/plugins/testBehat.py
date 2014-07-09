import unittest
import mock
import os

from plugins.behat import BehatPlugin
from xml.dom.minidom import parse, parseString

class TestBehatPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = BehatPlugin()

    def test_activate(self):
        self.assertEquals(self.plugin.activate(), "Behat plugin actif")

    def test_deactivate(self):
        self.assertEquals(self.plugin.deactivate(), "Behat plugin inactif")

    def test_getFileResult(self):
        self.assertEquals(self.plugin.getFileResult('script_a_lancer.feature'),'script_a_lancer')

    @unittest.skip('TODO')
    def test_loadConfigPlugin(self):
        pass

    @unittest.skip('TODO')
    def test_saveConfigPlugin(self):
        pass

    @unittest.skip('TODO')
    def test_loadConfigRunner(self):
        pass

    @unittest.skip('TODO')
    def test_saveConfigRunner(self):
        pass

    def test_run(self):
        os.system=mock.Mock(return_value=0)
        self.assertEquals(self.plugin.run('profile','script'),0)

    @mock.patch('plugins.behat.parse')
    def test_result_ok(self, mock_parse):
        xmlString = '''
        <testsuite classname="behat.features" errors="0" failures="0" name="test bidon" file="scenario.feature" tests="3" time="5.431202">
         <testcase classname="behat.feature" name="testcase bidon" time="5.430192">
         </testcase>
         </testsuite>
        '''
        xmlDocument = parseString(xmlString)
        mock_parse.return_value=xmlDocument
        self.assertEquals(self.plugin.result('profile','script'),('p',u'test bidon\ntestcase bidon\n   Temps execution : 5.430192\n\n'))

    @mock.patch('plugins.behat.parse')
    def test_result_nok(self, mock_parse):
        xmlString = '''
        <testsuite classname="behat.features" errors="0" failures="1" name="test bidon" file="scenario.feature" tests="3" time="5.431202">
         <testcase classname="behat.feature" name="testcase bidon" time="5.430192">
         </testcase>
         </testsuite>
        '''
        xmlDocument = parseString(xmlString)
        mock_parse.return_value=xmlDocument
        self.assertEquals(self.plugin.result('profile','script'),('f',u'test bidon\ntestcase bidon\n   Temps execution : 5.430192\n\n'))

    @mock.patch('plugins.behat.parse')
    def test_result_exception(self,mock_parse):
        e=IOError('fichier non trouve')
        mock_parse.side_effect=e
        self.assertEquals(self.plugin.result('profile','script'),('f','Tests sous profile non passe\n'))

    @mock.patch('plugins.behat.parse')
    def test_result_failure(self, mock_parse):
        xmlString = '''
        <testsuite classname="behat.features" errors="0" failures="1" name="name testsuite" file="scenario.feature" tests="11" time="0.034493">
            <testcase classname="classname" name="name testcase" time="0.033612">
            <failure message="Message failure" type="failed">
            <![CDATA[
                  Content
            ]]></failure>
            </testcase>
         </testsuite>
        '''
        xmlDocument = parseString(xmlString)
        mock_parse.return_value=xmlDocument
        self.assertEquals(self.plugin.result('profile','script'),('f',u'name testsuite\nname testcase\n   Temps execution : 0.033612\n      Erreur : Message failure\n\n'))
        
if __name__ == '__main__':
    unittest.main()
