#!/usr/bin/env python

import unittest
from securesubmit.tests.general import GeneralTests
from securesubmit.tests.visa import VisaTests
from securesubmit.tests.mastercard import MasterCardTests
from securesubmit.tests.amex import AmexTests
from securesubmit.tests.discover import DiscoverTests
from securesubmit.tests.batch_certification import BatchCertTests
from securesubmit.tests.certification import Certification
from securesubmit.tests.token_service import TokenServiceTests
from securesubmit.tests.ach_echeck import CheckTests
from securesubmit.tests.giftcard import GiftCardTests

"""Load Tests"""
general = unittest.TestLoader().loadTestsFromTestCase(GeneralTests)
visa = unittest.TestLoader().loadTestsFromTestCase(VisaTests)
mastercard = unittest.TestLoader().loadTestsFromTestCase(MasterCardTests)
amex = unittest.TestLoader().loadTestsFromTestCase(AmexTests)
discover = unittest.TestLoader().loadTestsFromTestCase(DiscoverTests)
batch_cert = unittest.TestLoader().loadTestsFromTestCase(BatchCertTests)
certification = unittest.TestLoader().loadTestsFromTestCase(Certification)
tokenization = unittest.TestLoader().loadTestsFromTestCase(TokenServiceTests)
giftcard = unittest.TestLoader().loadTestsFromTestCase(GiftCardTests)
ach_echeck = unittest.TestLoader().loadTestsFromTestCase(CheckTests)

"""Run Tests"""
unittest.TextTestRunner(verbosity=2).run(general)
unittest.TextTestRunner(verbosity=2).run(visa)
unittest.TextTestRunner(verbosity=2).run(mastercard)
unittest.TextTestRunner(verbosity=2).run(amex)
unittest.TextTestRunner(verbosity=2).run(discover)
unittest.TextTestRunner(verbosity=2).run(batch_cert)
unittest.TextTestRunner(verbosity=2).run(certification)
unittest.TextTestRunner(verbosity=2).run(tokenization)
unittest.TextTestRunner(verbosity=2).run(giftcard)
unittest.TextTestRunner(verbosity=2).run(ach_echeck)
