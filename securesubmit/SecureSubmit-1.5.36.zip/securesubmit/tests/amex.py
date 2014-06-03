import unittest
from enum import Enum
from securesubmit.tests.test_data \
    import (TestServicesConfig,
            TestCreditCard,
            TestCardHolder)
from securesubmit.services.gateway \
    import (HpsCreditService,
            HpsExceptionCodes,
            HpsCreditException,
            HpsTransactionDetails)


class AmexTests(unittest.TestCase):
    charge_service = HpsCreditService(
        TestServicesConfig.valid_services_config)

    def test_amex_charge(self):
        response = self._charge_valid_amex(50)
        self.assertEqual(response.response_code, "00")

    # AVS Tests
    def test_amex_avs_response_A(self):
        response = self._charge_valid_amex(90.01)
        self.assertEqual(response.avs_result_code, "A")

    def test_amex_avs_response_N(self):
        response = self._charge_valid_amex(90.02)
        self.assertEqual(response.avs_result_code, "N")

    def test_amex_avs_response_R(self):
        response = self._charge_valid_amex(90.03)
        self.assertEqual(response.avs_result_code, "R")

    def test_amex_avs_response_S(self):
        response = self._charge_valid_amex(90.04)
        self.assertEqual(response.avs_result_code, "S")

    def test_amex_avs_response_U(self):
        response = self._charge_valid_amex(90.05)
        self.assertEqual(response.avs_result_code, "U")

    def test_amex_avs_response_W(self):
        response = self._charge_valid_amex(90.06)
        self.assertEqual(response.avs_result_code, "W")

    def test_amex_avs_response_X(self):
        response = self._charge_valid_amex(90.07)
        self.assertEqual(response.avs_result_code, "X")

    def test_amex_avs_response_Y(self):
        response = self._charge_valid_amex(90.08)
        self.assertEqual(response.avs_result_code, "Y")

    def test_amex_avs_response_Z(self):
        response = self._charge_valid_amex(90.09)
        self.assertEqual(response.avs_result_code, "Z")

    # CVV Tests
    def test_amex_cvv_response_M(self):
        response = self._charge_valid_amex(97.01)
        self.assertEqual(response.cvv_result_code, "M")

    def test_amex_cvv_response_N(self):
        response = self._charge_valid_amex(97.02)
        self.assertEqual(response.cvv_result_code, "N")

    def test_amex_cvv_response_P(self):
        response = self._charge_valid_amex(97.03)
        self.assertEqual(response.cvv_result_code, "P")

    # Amex to Visa 2nd
    def test_amex_response_denied(self):
        try:
            response = self._charge_valid_amex(10.08)
        except HpsCreditException, e:
            self.assertEqual(HpsExceptionCodes.card_declined, e.code)
            return

        self.fail("No exception was thrown.")

    def test_amex_response_card_expired(self):
        try:
            response = self._charge_valid_amex(10.32)
        except HpsCreditException, e:
            self.assertEqual(HpsExceptionCodes.expired_card, e.code)
            return

        self.fail("No exception was thrown.")

    def test_amex_response_please_call(self):
        try:
            response = self._charge_valid_amex(10.34)
        except HpsCreditException, e:
            self.assertEqual(HpsExceptionCodes.card_declined, e.code)
            return

        self.fail("No exception was thrown.")

    def test_amex_response_invalid_merchant(self):
        try:
            response = self._charge_valid_amex(10.22)
        except HpsCreditException, e:
            self.assertEqual(HpsExceptionCodes.card_declined, e.code)
            return

        self.fail("No exception was thrown.")

    def test_amex_response_invalid_amount(self):
        try:
            response = self._charge_valid_amex(10.27)
        except HpsCreditException, e:
            self.assertEqual(HpsExceptionCodes.invalid_amount, e.code)
            return

        self.fail("No exception was thrown.")

    def test_amex_response_no_action_taken(self):
        try:
            response = self._charge_valid_amex(10.14)
        except HpsCreditException, e:
            self.assertEqual(HpsExceptionCodes.incorrect_number, e.code)
            return

        self.fail("No exception was thrown.")

    def test_amex_response_invalid_cvv2(self):
        try:
            response = self._charge_valid_amex(10.23)
        except HpsCreditException, e:
            self.assertEqual(HpsExceptionCodes.incorrect_cvc, e.code)
            return

        self.fail("No exception was thrown.")

    def test_amex_response_message_format_error(self):
        try:
            response = self._charge_valid_amex(10.06)
        except HpsCreditException, e:
            self.assertEqual(HpsExceptionCodes.processing_error, e.code)
            return

        self.fail("No exception was thrown.")

    def test_amex_response_invalid_originator(self):
        try:
            response = self._charge_valid_amex(10.30)
        except HpsCreditException, e:
            self.assertEqual(HpsExceptionCodes.processing_error, e.code)
            return

        self.fail("No exception was thrown.")

    def test_amex_response_card_declined(self):
        try:
            response = self._charge_valid_amex(10.25)
        except HpsCreditException, e:
            self.assertEqual(HpsExceptionCodes.card_declined, e.code)
            return

        self.fail("No exception was thrown.")

    def test_amex_response_account_cancelled(self):
        try:
            response = self._charge_valid_amex(10.13)
        except HpsCreditException, e:
            self.assertEqual(HpsExceptionCodes.card_declined, e.code)
            return

        self.fail("No exception was thrown.")

    def test_amex_response_merchant_close(self):
        try:
            response = self._charge_valid_amex(10.12)
        except HpsCreditException, e:
            self.assertEqual(HpsExceptionCodes.processing_error, e.code)
            return

        self.fail("No exception was thrown.")

    def test_amex_response_pickup_card(self):
        try:
            response = self._charge_valid_amex(10.04)
        except HpsCreditException, e:
            self.assertEqual(HpsExceptionCodes.card_declined, e.code)
            return

        self.fail("No exception was thrown.")

    # Verify, Authorize & Capture
    def test_amex_verify(self):
        response = self.charge_service.verify(
            TestCreditCard.valid_amex,
            TestCardHolder.valid_card_holder)
        self.assertEqual("00", response.response_code)

    def test_amex_authorize(self):
        response = self.charge_service.authorize(
            50, "usd",
            TestCreditCard.valid_amex,
            TestCardHolder.valid_card_holder)
        self.assertEqual("00", response.response_code)

    def test_amex_token_authorize(self):
        response = self.charge_service.authorize(
            50, "usd",
            TestCreditCard.valid_amex,
            TestCardHolder.valid_card_holder, True)
        self.assertEqual('0', response.token_data.token_rsp_code)
        self.assertEqual("00", response.response_code)

    def test_amex_capture(self):
        # Authorize the card.
        authResponse = self.charge_service.authorize(
            50, "usd",
            TestCreditCard.valid_amex,
            TestCardHolder.valid_card_holder)
        self.assertEqual("00", authResponse.response_code)

        # Capture the authorization.
        captureResponse = self.charge_service.capture(
            authResponse.transaction_id)
        self.assertEqual("00", captureResponse.response_code)

    # Helper Method
    def _charge_valid_amex(self, amt):
        response = self.charge_service.charge(
            amt, "usd",
            TestCreditCard.valid_amex,
            TestCardHolder.valid_card_holder)
        if response is None:
            self.fail("Response is null.")

        return response