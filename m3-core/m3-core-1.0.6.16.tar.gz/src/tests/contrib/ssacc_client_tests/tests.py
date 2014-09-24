#coding:utf-8
from xml.dom import minidom
from xml.dom.minidom import Element

from django.test.client import RequestFactory
from django.utils import unittest

from m3_ssacc_client.exceptions import SSACCException
from m3_ssacc_client.requests_to_server import server_ssacc_ping, server_ssacc_profile_rates
from m3_ssacc_client.results import BaseResult, ProfileRatesResult, AvailabilityResult
from m3_ssacc_client.views import (ssacc_ping, ssacc_profile_meta,
    ssacc_operator_meta, ssacc_license_meta, ssacc_operator_exists, ssacc_profile_new, ssacc_profile_edit, ssacc_operator_edit, ssacc_operator_new, ssacc_operator_delete, ssacc_profile_delete)

__author__ = 'daniil-ganiev'

###############################################################################
#Тестирование враппер-объектов
#####################################se##########################################

class BaseResultToProfileRatesResultTestCase(unittest.TestCase):

    def setUp(self):
        document = minidom.Document()
        result_node = document.createElement('result')
        document.appendChild(result_node)
        result_node.setAttribute('status', 'ok')
        param1 = Element('param')
        param1.setAttribute('code', '1')
        param1.setAttribute('min_value', 'trololo')
        param1.setAttribute('max_value', 'blobloblo')
        param2 = Element('param')
        param2.setAttribute('code', '2')
        param2.setAttribute('min_value', 'kakakak')
        param2.setAttribute('max_value', 'mimim')
        result_node.appendChild(param1)
        result_node.appendChild(param2)

        self.result = BaseResult.parse_xml_to_result(document.toxml(),
            ProfileRatesResult)

        xml_result = self.result.return_response()
        self.result_document = minidom.parseString(xml_result.content)

    def test_parseXmlToRequest_getsCorrectProfileRatesResultString_has2ParamNodes(self):
        params = self.result_document.getElementsByTagName('param')
        params = [param for param in params if param.getAttribute('code')
            in ('1','2')]
        self.assertEqual(len(params), 2)


class BaseResultToAvailabilityResultTestCase(unittest.TestCase):

    def setUp(self):
        document = minidom.Document()
        result_node = document.createElement('result')
        document.appendChild(result_node)
        result_node.setAttribute('status', 'ok')
        availability = Element('availability')
        availability.setAttribute('status', '0')
        availability.setAttribute('message', 'trololo')
        result_node.appendChild(availability)

        self.result = BaseResult.parse_xml_to_result(document.toxml(),
            AvailabilityResult)

        xml_result = self.result.return_response()
        self.result_document = minidom.parseString(xml_result.content)

    def test_parseXmlToRequest_getsCorrectAvailabilityResultString_hasAvailabilityNode(self):
        availabilities = self.result_document.getElementsByTagName('availability')
        availability = [a for a in availabilities
            if a.getAttribute('status') == '0'
            and a.getAttribute('message') == 'trololo']

        self.assertEqual(len(availability), 1)


###############################################################################
#Запросы на SSACC сервер
###############################################################################
#Пока нет сервака, на который можно было бы обращаться.

#class RequestsToServerTestCase(unittest.TestCase):
#
#    def test_ServerSsaccPing_runs_noExceptions(self):
#        server_ssacc_ping()
#
#    def test_ServerSsaccProfileRates_runs_noExceptions(self):
#        server_ssacc_profile_rates(account_id='1')

###############################################################################
#Результаты, которые запрашивает ссакосервак
###############################################################################
class BaseViewTestCase(object):
    request_address = ''

    def setUp(self, **kwargs):
        self.factory = RequestFactory()
        self.request = self.factory.post(self.request_address, kwargs)

    def test_View_runs_returnsXmlMimeType(self):
        self.assertEqual(self.response._headers['content-type'][1], 'text/xml')

    def test_View_runs_statusCodeIs200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_View_runs_resultStatusIsOk(self):
        document = minidom.parseString(self.response.content)
        result_nodes = document.getElementsByTagName('result')
        result_node = result_nodes[0]
        self.assertEqual(result_node.getAttribute('status'), 'ok')

    def test_View_runs_hasResultStatus(self):
        document = minidom.parseString(self.response.content)
        result_nodes = document.getElementsByTagName('result')
        self.assertNotEqual(len(result_nodes), 0)


class SsaccPingViewTestCase(BaseViewTestCase, unittest.TestCase):
    request_address = '/ssacc/ping'

    def setUp(self):
        super(SsaccPingViewTestCase, self).setUp()
        self.response = ssacc_ping(self.request)


class BaseProfileMetaViewTestCase(BaseViewTestCase):
    def test_View_runs_hasIntParam(self):
        document = minidom.parseString(self.response.content)
        result_nodes = document.getElementsByTagName('param')
        int_param_nodes = [node for node in result_nodes
            if node.getAttribute('type') == 'int'
            and node.getAttribute('code') == 'code1']
        self.assertEqual(len(int_param_nodes), 1)

    def test_View_runs_hasListItems(self):
        document = minidom.parseString(self.response.content)
        result_nodes = document.getElementsByTagName('param')
        list_param_nodes = [node for node in result_nodes
            if node.getAttribute('type') == 'list'
            and node.getAttribute('code') == 'code4']
        list_node = list_param_nodes[0]
        list_node_items = list_node.getElementsByTagName('item')

        self.assertEqual(len(list_node_items), 2)


class SsaccProfileMetaViewTestCase(BaseProfileMetaViewTestCase,
    unittest.TestCase):
    request_address = '/ssacc/profile/meta'

    def setUp(self):
        super(SsaccProfileMetaViewTestCase, self).setUp()
        self.response = ssacc_profile_meta(self.request)


class SsaccOperatorMetaViewTestCase(BaseProfileMetaViewTestCase,
    unittest.TestCase):
    request_address = '/ssacc/operator/meta'

    def setUp(self):
        super(SsaccOperatorMetaViewTestCase, self).setUp()
        self.response = ssacc_operator_meta(self.request)


class SsaccLicenseMetaViewTestCase(BaseViewTestCase, unittest.TestCase):
    request_address = '/ssacc/license/meta'

    def setUp(self):
        super(SsaccLicenseMetaViewTestCase, self).setUp()
        self.response = ssacc_license_meta(self.request)

    def test_runs_hasCertainObjectNode(self):
        document = minidom.parseString(self.response.content)
        result_nodes = document.getElementsByTagName('object')
        object_nodes = [node for node in result_nodes
            if node.getAttribute('type') == 'int'
            and node.getAttribute('code') == 'obj_code'
            and node.getAttribute('name') == 'obj_name']

        self.assertEqual(len(object_nodes), 1)

    def test_runs_has2ObjectNodes(self):
        document = minidom.parseString(self.response.content)
        object_nodes = document.getElementsByTagName('object')

        self.assertEqual(len(object_nodes), 2)


class SsaccOperatorExistsViewTestCase(BaseViewTestCase, unittest.TestCase):
    request_address = '/ssacc/operator/exists'
    def setUp(self):
        super(SsaccOperatorExistsViewTestCase, self).setUp(login = 'ololo')

        self.response = ssacc_operator_exists(self.request)

    def test_getsNoLogin_raisesSSACCException(self):
        request = self.factory.post(self.request_address)
        
        with self.assertRaises(SSACCException):
            response = ssacc_operator_exists(request)

    def test_runs_hasOperatorNode(self):
        document = minidom.parseString(self.response.content)
        result_nodes = document.getElementsByTagName('operator')
        operator_nodes = [node for node in result_nodes
            if node.getAttribute('account_id') == 'some_account'
            and node.getAttribute('login') == 'ololo']

        self.assertEqual(len(operator_nodes), 1)


class SsaccProfileNewViewTestCase(BaseViewTestCase, unittest.TestCase):
    request_address = '/ssacc/profile/new'
    def setUp(self, **kwargs):
        super(SsaccProfileNewViewTestCase, self).setUp(login='ololo',
            account_id='account_id', enc_password='md5$blah$blah')
        self.response = ssacc_profile_new(self.request)

    def test_noLogin_raisesSsaccException(self):
        request = self.factory.post(self.request_address)

        with self.assertRaises(SSACCException):
            response = ssacc_profile_new(request)

    def test_noAccountid_raisesSsaccException(self):
        request = self.factory.post(self.request_address, dict(login='ty'))

        with self.assertRaises(SSACCException):
            response = ssacc_profile_new(request)

    def test_noPasswords_raisesSsaccException(self):
        request = self.factory.post(self.request_address, dict(login='ty',
            account_id='sdf'))

        with self.assertRaises(SSACCException):
            response = ssacc_profile_new(request)

    def test_onlyRawPassword_noExceptions(self):
        request = self.factory.post(self.request_address, dict(login='ty',
            account_id='sdf', raw_password='sdf'))

        response = ssacc_profile_new(request)

    def test_wrongEncPassword_raisesSsaccException(self):
        request = self.factory.post(self.request_address, dict(login='ty',
            account_id='sdf', enc_password='wrong'))

        with self.assertRaises(SSACCException):
            response = ssacc_profile_new(request)


class SsaccProfileEditViewTestCase(BaseViewTestCase, unittest.TestCase):
    request_address = '/ssacc/profile/edit'
    def setUp(self, **kwargs):
        super(SsaccProfileEditViewTestCase, self).setUp(login='ololo',
            account_id='account_id', enc_password='md5$blah$blah')
        self.response = ssacc_profile_edit(self.request)

    def test_noLogin_raisesSsaccException(self):
        request = self.factory.post(self.request_address)

        with self.assertRaises(SSACCException):
            response = ssacc_profile_edit(request)

    def test_noAccountid_raisesSsaccException(self):
        request = self.factory.post(self.request_address, dict(login='ty'))

        with self.assertRaises(SSACCException):
            response = ssacc_profile_edit(request)

    def test_noPasswords_raisesSsaccException(self):
        request = self.factory.post(self.request_address, dict(login='ty',
            account_id='sdf'))

        with self.assertRaises(SSACCException):
            response = ssacc_profile_edit(request)

    def test_onlyRawPassword_noExceptions(self):
        request = self.factory.post(self.request_address, dict(login='ty',
            account_id='sdf', raw_password='sdf'))

        response = ssacc_profile_edit(request)

    def test_wrongEncPassword_raisesSsaccException(self):
        request = self.factory.post(self.request_address, dict(login='ty',
            account_id='sdf', enc_password='wrong'))

        with self.assertRaises(SSACCException):
            response = ssacc_profile_edit(request)


class SsaccOperatorNewViewTestCase(BaseViewTestCase, unittest.TestCase):
    request_address = '/ssacc/operator/new'
    def setUp(self, **kwargs):
        super(SsaccOperatorNewViewTestCase, self).setUp(login='ololo',
            account_id='account_id', enc_password='md5$blah$blah')
        self.response = ssacc_operator_new(self.request)

    def test_noLogin_raisesSsaccException(self):
        request = self.factory.post(self.request_address)

        with self.assertRaises(SSACCException):
            response = ssacc_operator_new(request)

    def test_noAccountid_raisesSsaccException(self):
        request = self.factory.post(self.request_address, dict(login='ty'))

        with self.assertRaises(SSACCException):
            response = ssacc_operator_new(request)

    def test_noPasswords_raisesSsaccException(self):
        request = self.factory.post(self.request_address, dict(login='ty',
            account_id='sdf'))

        with self.assertRaises(SSACCException):
            response = ssacc_operator_new(request)

    def test_onlyRawPassword_noExceptions(self):
        request = self.factory.post(self.request_address, dict(login='ty',
            account_id='sdf', raw_password='sdf'))

        response = ssacc_operator_new(request)

    def test_wrongEncPassword_raisesSsaccException(self):
        request = self.factory.post(self.request_address, dict(login='ty',
            account_id='sdf', enc_password='wrong'))

        with self.assertRaises(SSACCException):
            response = ssacc_operator_new(request)

            
class SsaccOperatorEditViewTestCase(BaseViewTestCase, unittest.TestCase):
    request_address = '/ssacc/operator/edit'
    def setUp(self, **kwargs):
        super(SsaccOperatorEditViewTestCase, self).setUp(login='ololo',
            account_id='account_id', enc_password='md5$blah$blah')
        self.response = ssacc_operator_edit(self.request)

    def test_noLogin_raisesSsaccException(self):
        request = self.factory.post(self.request_address)

        with self.assertRaises(SSACCException):
            response = ssacc_operator_edit(request)

    def test_noAccountid_raisesSsaccException(self):
        request = self.factory.post(self.request_address, dict(login='ty'))

        with self.assertRaises(SSACCException):
            response = ssacc_operator_edit(request)

    def test_noPasswords_raisesSsaccException(self):
        request = self.factory.post(self.request_address, dict(login='ty',
            account_id='sdf'))

        with self.assertRaises(SSACCException):
            response = ssacc_operator_edit(request)

    def test_onlyRawPassword_noExceptions(self):
        request = self.factory.post(self.request_address, dict(login='ty',
            account_id='sdf', raw_password='sdf'))

        response = ssacc_operator_edit(request)

    def test_wrongEncPassword_raisesSsaccException(self):
        request = self.factory.post(self.request_address, dict(login='ty',
            account_id='sdf', enc_password='wrong'))

        with self.assertRaises(SSACCException):
            response = ssacc_operator_edit(request)


class SsaccProfileDeleteViewTestCase(BaseViewTestCase, unittest.TestCase):
    request_address = '/ssacc/profile/delete'
    def setUp(self, **kwargs):
        super(SsaccProfileDeleteViewTestCase, self).setUp(account_id='1')

        self.response = ssacc_profile_delete(self.request)

    def test_noAccountId_raisesSsaccException(self):
        request = self.factory.post(self.request_address)

        with self.assertRaises(SSACCException):
            response = ssacc_profile_delete(request)


class SsaccOperatorDeleteViewTestCase(BaseViewTestCase, unittest.TestCase):
    request_address = '/ssacc/operator/delete'
    def setUp(self, **kwargs):
        super(SsaccOperatorDeleteViewTestCase, self).setUp(account_id='1')

        self.response = ssacc_operator_delete(self.request)

    def test_noAccountId_raisesSsaccException(self):
        request = self.factory.post(self.request_address)

        with self.assertRaises(SSACCException):
            response = ssacc_operator_delete(request)