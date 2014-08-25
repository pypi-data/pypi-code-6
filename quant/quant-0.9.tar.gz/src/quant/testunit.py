import unittest
from dm.testunit import ApplicationTestSuite
from dm.testunit import TestCase
from quant.builder import ApplicationBuilder

VOLATILITY_MEDIUM = 1.0
VOLATILITY_LOW = 0.3333
VOLATILITY_HIGH = 3.0
VOLATILITY_ZERO = 0.00001

class TestCase(TestCase):
    "Base class for quant TestCases."

    pass
    # @classmethod
    # def setUpClass(cls):
    #     if cls.__name__.endswith('TestCase'):
    #         raise unittest.SkipTest("Skip base class tests: %s" % cls)
    #     super(TestCase, cls).setUpClass()


class ApplicationTestSuite(ApplicationTestSuite):
    appBuilderClass = ApplicationBuilder

