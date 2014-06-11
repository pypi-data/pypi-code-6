import unittest
import datetime
from securesubmit.services.gateway import (HpsCreditService,
                                           HpsTransactionType,
                                           HpsExceptionCodes,
                                           HpsInvalidRequestException,
                                           HpsAuthenticationException,
                                           HpsCreditException,
                                           HpsGatewayException)
from securesubmit.tests.test_data import (TestCreditCard,
                                          TestCardHolder,
                                          TestServicesConfig)


class GeneralTests(unittest.TestCase):
    charge_service = HpsCreditService()

    def test_charge_invalid_amount(self):
        charge_amount = -5
        self.charge_service._config = None

        try:
            self.charge_service.charge(
                charge_amount, "usd",
                TestCreditCard.valid_visa,
                TestCardHolder.valid_card_holder)
        except HpsInvalidRequestException, e:
            self.assertEquals(e.code, HpsExceptionCodes.invalid_amount)
            self.assertEquals(e.param_name, 'amount')
            return

        self.fail("No exception was raised")

    def test_charge_empty_currency(self):
        charge_amount = 50
        currency = ""
        self.charge_service._config = None

        try:
            self.charge_service.charge(
                charge_amount, currency,
                TestCreditCard.valid_visa,
                TestCardHolder.valid_card_holder)
        except HpsInvalidRequestException, e:
            self.assertEquals(e.code, HpsExceptionCodes.missing_currency)
            self.assertEquals(e.param_name, "currency")
            return

        self.fail("No exception was raised")

    def test_charge_no_currency(self):
        charge_amount = 50
        currency = "EUR"
        self.charge_service._config = None

        try:
            self.charge_service.charge(
                charge_amount, currency,
                TestCreditCard.valid_visa,
                TestCardHolder.valid_card_holder)
        except HpsInvalidRequestException, e:
            self.assertEquals(e.code, HpsExceptionCodes.invalid_currency)
            self.assertEquals(e.param_name, 'currency')
            return

        self.fail("No exception was thrown.")

    def test_charge_invalid_config(self):
        charge_amount = 50
        currency = "usd"
        self.charge_service.services_config = None

        try:
            self.charge_service.charge(
                charge_amount, currency,
                TestCreditCard.valid_visa,
                TestCardHolder.valid_card_holder)
        except HpsAuthenticationException, e:
            self.assertIn(
                e.message,
                ('The HPS SDK has not been properly configured. '
                 'Please make sure to initialize the config either '
                 'in a service constructor or in your App.config '
                 'or Web.config file.'))
            return

        self.fail("No exception was thrown.")

    def test_charge_invalid_card_number(self):
        charge_amount = 50
        currency = "usd"
        self.charge_service._config = TestServicesConfig.valid_services_config

        try:
            self.charge_service.charge(
                charge_amount, currency,
                TestCreditCard.invalid_card,
                TestCardHolder.valid_card_holder)
        except (HpsCreditException, HpsGatewayException) as e:
            self.assertEqual(e.code, HpsExceptionCodes.invalid_number)
            return

        self.fail("No exception was thrown.")

    def test_list_should_list(self):
        self.charge_service._config = TestServicesConfig.valid_services_config

        items = self.charge_service.list(
            datetime.datetime.utcnow() + datetime.timedelta(-10),
            datetime.datetime.utcnow())
        self.assertIsNotNone(items)

    def test_list_should_list_filter(self):
        self.charge_service._config = TestServicesConfig.valid_services_config

        items = self.charge_service.list(
            datetime.datetime.utcnow() + datetime.timedelta(-10),
            datetime.datetime.utcnow(), HpsTransactionType.Capture)
        self.assertIsNotNone(items)

    def test_get_first_charge(self):
        self.charge_service._config = TestServicesConfig.valid_services_config
        items = self.charge_service.list(
            datetime.datetime.utcnow() + datetime.timedelta(-10),
            datetime.datetime.utcnow())

        if len(items) > 0:
            charge = self.charge_service.get(items[0].transaction_id)
            self.assertIsNotNone(charge)