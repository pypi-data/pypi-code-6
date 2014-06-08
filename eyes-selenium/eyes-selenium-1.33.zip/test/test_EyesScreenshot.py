import unittest

from applitools.errors import EyesError
from applitools._webdriver import EyesScreenshot


class MockWebDriver(object):
    pass


class EyesScreenshotInit(unittest.TestCase):
    """
    Tests EyesScreenshot initialization.
    """
    def setUp(self):
        self.driver = MockWebDriver()

    def test_no_screenshot(self):
        self.assertRaises(EyesError, EyesScreenshot, self.driver)
