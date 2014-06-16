from email_phone_block import block
import unittest


class TestBlock(unittest.TestCase):

    def setUp(self):
        pass

    def test_email_1(self):
        self.assertEqual(block("name@domain.com"), "xxxx@xxxxx.xxx")

    def test_email_2(self):
        self.assertEqual(block("name(at)domain.com"), "xxxx@xxxxx.xxx")

    def test_email_3(self):
        self.assertEqual(block("name at domain.com"), "xxxx@xxxxx.xxx")

    def test_phone_1(self):
        self.assertEqual(block("333 333 3333"), "xxx-xxx-xxxx")

    def test_phone_2(self):
        self.assertEqual(block("333-333-3333"), "xxx-xxx-xxxx")

    def test_phone_3(self):
        self.assertEqual(block("333 333-3333"), "xxx-xxx-xxxx")

    def test_phone_4(self):
        self.assertEqual(block("333-333 3333"), "xxx-xxx-xxxx")

    def test_phone_5(self):
        self.assertEqual(block("333-3333333"), "xxx-xxx-xxxx")

    def test_phone_6(self):
        self.assertEqual(block("333333-3333"), "xxx-xxx-xxxx")

    def test_phone_7(self):
        self.assertEqual(block("3333333333"), "xxx-xxx-xxxx")


if __name__ == '__main__':
    unittest.main()