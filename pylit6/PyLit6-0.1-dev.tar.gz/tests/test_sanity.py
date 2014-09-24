import unittest

class TestSanity(unittest.TestCase):

    def setUp(self):
        pass

    def test_sanity(self):
        self.assertEqual(1, 1)

    def tearDown(self):
        pass

if __name__ =='__main__':
    unittest.main()

