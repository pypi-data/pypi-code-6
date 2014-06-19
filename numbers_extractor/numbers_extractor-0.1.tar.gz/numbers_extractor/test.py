from numbers_extractor import numbers_extractor
import unittest


class TestNumberExtractor(unittest.TestCase):

    def setUp(self):
        pass

    def test_string_1(self):
        self.assertEqual(numbers_extractor("20 is 10 plus 10"), [20, 10, 10])

    def test_string_2(self):
        self.assertEqual(numbers_extractor("20 is 10 plus 10", multiple=False), 20)

    def test_string_3(self):
        self.assertEqual(numbers_extractor("no numbers here"), [])

    def test_string_4(self):
        self.assertEqual(numbers_extractor("no numbers here", multiple=False), None)


if __name__ == '__main__':
    unittest.main()