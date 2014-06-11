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
            HpsException,
            HpsBatchService)


class BatchCertTests(unittest.TestCase):
    batch_service = HpsBatchService(TestServicesConfig.valid_services_config)
    charge_service = HpsCreditService(TestServicesConfig.valid_services_config)

    def test_inline_certification(self):
        self.Batch_ShouldClose_Ok()
        self.Visa_ShouldCharge_Ok()
        self.MasterCard_ShouldCharge_Ok()
        self.Discover_ShouldCharge_Ok()
        self.Amex_ShouldCharge_Ok()
        self.Jcb_ShouldCharge_Ok()
        self.Visa_ShouldVerify_Ok()
        self.MasterCard_ShouldVerify_Ok()
        self.Discover_ShouldVerify_Ok()
        self.Amex_Avs_ShouldVerify_Ok()
        self.Mastercard_Return_ShouldBe_Ok()
        self.Visa_ShouldReverse_Ok()
        self.Batch_ShouldClose_Ok()

    def Batch_ShouldClose_Ok(self):
        try:
            response = self.batch_service.close_batch()
            if response is None:
                self.fail("Response is None")
        except HpsException, e:
            if e.code != HpsExceptionCodes.no_open_batch:
                self.fail("Something failed other than 'no open batch'.")

    def Visa_ShouldCharge_Ok(self):
        response = self.charge_service.charge(
            17.01, "usd",
            TestCreditCard.valid_visa,
            TestCardHolder.cert_holder_short_zip)
        if response is None:
            self.fail("Response is None")

        self.assertEqual(response.response_code, "00")

    def MasterCard_ShouldCharge_Ok(self):
        response = self.charge_service.charge(
            17.02, "usd",
            TestCreditCard.valid_mastercard,
            TestCardHolder.cert_holder_short_zip_no_street)
        if response is None:
            self.fail("Response is None")

        self.assertEqual(response.response_code, "00")

    def Discover_ShouldCharge_Ok(self):
        response = self.charge_service.charge(
            17.03, "usd",
            TestCreditCard.valid_discover,
            TestCardHolder.cert_holder_long_zip_no_street)
        if response is None:
            self.fail("Response is None")

        self.assertEqual(response.response_code, "00")

    def Amex_ShouldCharge_Ok(self):
        response = self.charge_service.charge(
            17.04, "usd",
            TestCreditCard.valid_amex,
            TestCardHolder.cert_holder_short_zip)
        if response is None:
            self.fail("Response is None")

        self.assertEqual(response.response_code, "00")

    def Jcb_ShouldCharge_Ok(self):
        response = self.charge_service.charge(
            17.05, "usd",
            TestCreditCard.valid_jcb,
            TestCardHolder.cert_holder_long_zip)
        if response is None:
            self.fail("Response is None")

        self.assertEqual(response.response_code, "00")

    def Visa_ShouldVerify_Ok(self):
        response = self.charge_service.verify(TestCreditCard.valid_visa)
        if response is None:
            self.fail("Response is None")

        self.assertEqual(response.response_code, "85")

    def MasterCard_ShouldVerify_Ok(self):
        response = self.charge_service.verify(TestCreditCard.valid_visa)
        if response is None:
            self.fail("Response is None")

        self.assertEqual(response.response_code, "85")

    def Discover_ShouldVerify_Ok(self):
        response = self.charge_service.verify(TestCreditCard.valid_visa)
        if response is None:
            self.fail("Response is None")

        self.assertEqual(response.response_code, "85")

    def Amex_Avs_ShouldVerify_Ok(self):
        response = self.charge_service.verify(
            TestCreditCard.valid_visa,
            TestCardHolder.cert_holder_short_zip_no_street)
        if response is None:
            self.fail("Response is None")

        self.assertEqual(response.response_code, "85")

    def Mastercard_Return_ShouldBe_Ok(self):
        response = self.charge_service.refund(
            15.15, "usd",
            TestCreditCard.valid_mastercard,
            TestCardHolder.cert_holder_short_zip)
        if response is None:
            self.fail("Response is None")

        self.assertEqual(response.response_code, "00")

    def Visa_ShouldReverse_Ok(self):
        response = self.charge_service.reverse(
            TestCreditCard.valid_visa,
            17.01, "usd")
        if response is None:
            self.fail("Response is None")

        self.assertEqual(response.response_code, "00")