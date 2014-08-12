import unittest
from shortid import ShortId

class TestShortId(unittest.TestCase):
    def setUp(self):
        self.shortid = ShortId()

    def test_should_be_unambiquous_on_a_bunch_of_iterations(self):
        ids = []
        for i in range(0, 50000):
            ids.append(self.shortid.generate())

        self.assertEqual(len(set(ids)), len(ids))
