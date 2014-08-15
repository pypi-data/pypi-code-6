import unittest
from copy import deepcopy
from datetime import datetime

import six
from mock import MagicMock

from gagrab import Grabber, data_from_query_response


class Test_Grabber(unittest.TestCase):
    def test_init(self):
        core = Grabber(authorized_service=MagicMock())
        self.assertTrue(core.project_id)
        self.assertTrue(core.service)


class Test_Grabber_query(unittest.TestCase):
    def setUp(self):
        self.core = Grabber(authorized_service=MagicMock())
        self.response = {
            u'itemsPerPage': 5,
            u'columnHeaders': [
                {u'columnType': u'DIMENSION', u'dataType': u'STRING', u'name': u'ga:dimension1'},
                {u'columnType': u'METRIC', u'dataType': u'INTEGER', u'name': u'ga:pageviews'}],
            u'rows': [[u'jeff|23', u'28'], [u'erik|116', u'12'], [u'amx|5', u'6'],
                      [u'amx|7', u'6'], [u'__default__|23', u'4']],
        }

    def test_arg_formating(self):
        ga_get_mock = MagicMock()
        ga_get_mock.return_value.execute.return_value = self.response
        self.core.service.data.return_value.ga.return_value.get = ga_get_mock
        self.core.query(
            view=555,
            dimensions=['dimension1'],
            metrics=['pageviews', 'othermetric'],
            start_date='2012-01-01',
            end_date='2014-01-01',
        )
        ga_get_mock.assert_called_with(
            ids='ga:555',
            dimensions='ga:dimension1',
            metrics='ga:pageviews,ga:othermetric',
            start_date='2012-01-01',
            end_date='2014-01-01'
        )

    def test_start_end_date_conversion(self):
        ga_get_mock = MagicMock()
        ga_get_mock.return_value.execute.return_value = self.response
        self.core.service.data.return_value.ga.return_value.get = ga_get_mock
        self.core.query(
            view=555,
            dimensions=['dimension1'],
            metrics=['pageviews', 'othermetric'],
            start_date=datetime(2012, 1, 1),
            end_date=datetime(2014, 1, 1),
        )
        ga_get_mock.assert_called_with(
            ids='ga:555',
            dimensions='ga:dimension1',
            metrics='ga:pageviews,ga:othermetric',
            start_date='2012-01-01',
            end_date='2014-01-01'
        )

    def test_depages_results(self):
        response2 = deepcopy(self.response)
        self.response['nextLink'] = 'a link'
        ga_get_mock = MagicMock()
        ga_get_mock.return_value.execute.side_effect = [self.response, response2]
        self.core.service.data.return_value.ga.return_value.get = ga_get_mock
        res = self.core.query(
            view=555,
            dimensions=['dimension1'],
            metrics=['pageviews', 'othermetric'],
            start_date=datetime(2012, 1, 1),
            end_date=datetime(2014, 1, 1),
        )
        self.assertEqual(len(res), 10)


class Test_data_from_query_response(unittest.TestCase):
    def setUp(self):
        """Have a sample query response with each datatype that we may be
        expected to convert.
        """
        self.query_response = {
            u'columnHeaders': [
                {u'columnType': u'DIMENSION', u'dataType': u'STRING', u'name': u'ga:operatingSystem'},
                {u'columnType': u'METRIC', u'dataType': u'INTEGER', u'name': u'ga:pageviews'},
                {u'columnType': u'METRIC', u'dataType': u'FLOAT', u'name': u'ga:pageviewsPerSession'},
                {u'columnType': u'METRIC', u'dataType': u'CURRENCY', u'name': u'ga:pagevalue'},
                {u'columnType': u'METRIC', u'dataType': u'TIME', u'name': u'ga:timeOnPage'},
                {u'columnType': u'METRIC', u'dataType': u'PERCENT', u'name': u'ga:percentNewSessions'}],
            u'containsSampledData': False,
            u'itemsPerPage': 10,
            u'kind': u'analytics#gaData',
            u'query': {
                u'dimensions': u'ga:operatingSystem',
                u'end-date': u'2014-05-12',
                u'ids': u'ga:71100146',
                u'max-results': 10,
                u'metrics': [
                    u'ga:pageviews', u'ga:pageviewsPerSession', u'ga:pagevalue',
                    u'ga:timeOnPage', u'ga:percentNewSessions'],
                u'sort': [u'-ga:pageviews'],
                u'start-date': u'2012-01-01',
                u'start-index': 1},
            u'rows': [
                [u'Windows', u'639691', u'4.84416223666076', u'0.0', u'9.7445507E7', u'3.749981068350826'],
                [u'Macintosh', u'47769', u'5.450593336376084', u'0.0', u'4357545.0', u'33.64901871291648'],
                [u'iOS', u'9694', u'2.3563441905687896', u'0.0', u'548628.0', u'41.00631988332523'],
                [u'Linux', u'1912', u'3.6628352490421454', u'0.0', u'160225.0', u'51.91570881226054'],
                [u'Android', u'426', u'1.8849557522123894', u'0.0', u'15291.0', u'66.8141592920354'],
                [u'Chrome OS', u'72', u'4.0', u'0.0', u'2413.0', u'55.55555555555556'],
                [u'Google TV', u'10', u'3.3333333333333335', u'0.0', u'1584.0', u'66.66666666666666'],
                [u'BlackBerry', u'2', u'1.0', u'0.0', u'0.0', u'100.0'],
                [u'Windows Phone', u'2', u'1.0', u'0.0', u'0.0', u'100.0']],
            u'totalResults': 9,
            u'totalsForAllResults': {
                u'ga:pagevalue': u'0.0', u'ga:pageviews': u'699578', u'ga:pageviewsPerSession': u'4.8013314573967945',
                u'ga:percentNewSessions': u'6.881026732095672', u'ga:timeOnPage': u'1.02531193E8'}}

    def test_corrent_number_rows(self):
        data = data_from_query_response(self.query_response)
        expected_num_rows = 9
        self.assertEqual(len(data), expected_num_rows)

    def test_string_conversion(self):
        data = data_from_query_response(self.query_response)
        self.assertIsInstance(data[0]['operatingSystem'], six.text_type)

    def test_integer_conversion(self):
        data = data_from_query_response(self.query_response)
        self.assertIsInstance(data[0]['pageviews'], int)

    def test_float_conversion(self):
        data = data_from_query_response(self.query_response)
        self.assertIsInstance(data[0]['pageviewsPerSession'], float)

    def test_currency_conversion(self):
        data = data_from_query_response(self.query_response)
        self.assertIsInstance(data[0]['pagevalue'], float)

    def test_time_conversion(self):
        data = data_from_query_response(self.query_response)
        self.assertIsInstance(data[0]['timeOnPage'], float)

    def test_percent_conversion(self):
        data = data_from_query_response(self.query_response)
        self.assertIsInstance(data[0]['percentNewSessions'], float)
