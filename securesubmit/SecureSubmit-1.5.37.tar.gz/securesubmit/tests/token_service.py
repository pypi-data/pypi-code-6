import unittest
import copy
from securesubmit.tests.test_data \
    import (TestServicesConfig,
            TestCreditCard,
            TestCardHolder)
from securesubmit.services.gateway \
    import (HpsCreditService,
            HpsCreditCard)
from securesubmit.services.token import HpsTokenService


class TokenServiceTests(unittest.TestCase):
    token_service = HpsTokenService(
        TestServicesConfig.valid_services_config.credential_token)

    def test_null_public_key(self):
        with self.assertRaises(TypeError):
            HpsTokenService(None)

    def test_empty_public_key(self):
        with self.assertRaises(TypeError):
            HpsTokenService('')

    def test_malformed_public_key(self):
        with self.assertRaises(TypeError):
            HpsTokenService('pkapi_bad')

    def test_bad_public_key(self):
        token = HpsTokenService(
            'pkapi_foo_foo').get_token(
                TestCreditCard.valid_visa)
        self.assertIsNotNone(token)

    def test_validation_invalid_card_number(self):
        card = HpsCreditCard()
        card.number = '1'

        response = self.token_service.get_token(card)
        error = response.error

        self.assertIsNotNone(error)
        self.assertEqual('2', error.code)
        self.assertEqual('card.number', error.param)
        self.assertEqual('Card number is invalid.', error.message)

    def test_validation_long_card_number(self):
        card = HpsCreditCard()
        card.number = '11111111111111111111111111111111111'

        response = self.token_service.get_token(card)
        error = response.error

        self.assertIsNotNone(error)
        self.assertEqual('2', error.code)
        self.assertEqual('card.number', error.param)
        self.assertEqual('Card number is invalid.', error.message)

    def test_validation_high_exp_month(self):
        card = copy.deepcopy(TestCreditCard.valid_visa)
        card.exp_month = 13

        response = self.token_service.get_token(card)
        error = response.error

        self.assertIsNotNone(error)
        self.assertEqual('2', error.code)
        self.assertEqual('card.exp_month', error.param)
        self.assertEqual('Card expiration month is invalid.', error.message)

    def test_validation_low_exp_year(self):
        card = copy.deepcopy(TestCreditCard.valid_visa)
        card.exp_year = 12

        response = self.token_service.get_token(card)
        error = response.error

        self.assertIsNotNone(error)
        self.assertEqual('2', error.code)
        self.assertEqual('card.exp_year', error.param)
        self.assertEqual('Card expiration year is invalid.', error.message)

    def test_validation_year_under_2000(self):
        card = copy.deepcopy(TestCreditCard.valid_visa)
        card.exp_year = 1999

        response = self.token_service.get_token(card)
        error = response.error

        self.assertIsNotNone(error)
        self.assertEqual('2', error.code)
        self.assertEqual('card.exp_year', error.param)
        self.assertEqual('Card expiration year is invalid.', error.message)

    def test_token_result(self):
        response = self.token_service.get_token(TestCreditCard.valid_visa)
        self.assertIsNone(response.error)

    def test_token_data_result(self):
        response = self.token_service.get_token(TestCreditCard.valid_visa)
        self.assertIsNotNone(response.token_value)
        self.assertIsNotNone(response.token_type)
        self.assertIsNotNone(response.token_expire)

    def test_token_charge(self):
        token = self.token_service.get_token(
            TestCreditCard.valid_visa)
        chargeService = HpsCreditService(
            TestServicesConfig.valid_services_config)
        charge = chargeService.charge(
            1, 'USD',
            token.token_value,
            TestCardHolder.valid_card_holder)

        self.assertIsNotNone(charge.authorization_code)