import unittest, RPIO
from hautomation_gpio.utils import *
from hautomation_gpio.cmds import *


TEST_WITH = 31


class TestGPIO(unittest.TestCase):

    def test_validate_address(self):
        self.assertRaises(
            ValueError,
            validate_address,
            100)
        self.assertTrue(
            validate_address(TEST_WITH),
            "Not properly validating address, as returns 26 as a not valid GPIO PIN")

    def test_set_output(self):
        set_to_output(TEST_WITH)
        self.assertTrue(
            RPIO.gpio_function(TEST_WITH) == RPIO.OUT,
            "Not properly changing GPIO26 to OUTPUT mode")

    def test_switch(self):
        set_to_output(TEST_WITH)
        pl_switch(TEST_WITH, "off")
        self.assertFalse(
            RPIO.forceinput(TEST_WITH),
            "Not properly turning off GPIO%s" % TEST_WITH)
        pl_switch(TEST_WITH, "on")
        self.assertTrue(
            RPIO.forceinput(TEST_WITH),
            "Not properly turning on GPIO%s" % TEST_WITH)
        pl_switch(TEST_WITH, "off")
        self.assertFalse(
            RPIO.forceinput(TEST_WITH),
            "Not properly turning off GPIO%s" % TEST_WITH)


  #TODO rest of the tests


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGPIO)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    unittest.main()
