import unittest
from run import run
from mock import patch, Mock


class CLIRunnerTests(unittest.TestCase):
    """Test suite for aggregator CLI runner"""
    @patch('run.imp')
    @patch('run.CoberturaJSONAggregator')
    @patch('run.CoberturaXMLAggregator')
    @patch('run.argparse')
    def test_runner(self, argparse_mock, xml_mock, api_mock, imp_mock):
        """XML and API type running configs"""
        mock_settings = Mock()
        mock_settings.SETTINGS = {'test': {'TYPE': 'xml'}}
        imp_mock.load_source.return_value = mock_settings
        xml_mock.TYPE_KEY = 'TYPE'
        run('')

        xml_mock().set_settings.assert_called_once_with(
            'test', {'TYPE': 'xml'}
        )
        xml_mock().generate_report.assert_called_once()
        xml_mock().print_report.assert_called_once()

        mock_settings.SETTINGS = {'test': {'TYPE': 'jenkins_api'}}
        imp_mock.load_source.return_value = mock_settings
        run('')

        api_mock().set_settings.assert_called_once_with(
            'test', {'TYPE': 'jenkins_api'}
        )
        api_mock().generate_report.assert_called_once()
        api_mock().print_report.assert_called_once()

        mock_settings.SETTINGS = {'test': {'TYPE': 'test'}}
        imp_mock.load_source.return_value = mock_settings
        self.assertRaises(UnboundLocalError, run, '')
