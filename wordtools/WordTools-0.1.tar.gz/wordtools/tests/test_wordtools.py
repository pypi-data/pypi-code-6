import unittest
import numpy as np

from wordtools import utils

class TestWordtoArray(unittest.TestCase):
    def test_wordtoarray_basic_usage(self):
        data = ["ab", "cd"]
        expect = np.array(["a", "b", "c", "d"], dtype="S1").reshape(2, 2)
        result = utils.wordtoarray(data, 2)
        np.testing.assert_array_equal(expect, result)

    def test_wordtoarray_short_words_get_padded(self):
        data = ["a", "cd"]
        expect = np.array(["a", " ", "c", "d"], dtype="S1").reshape(2, 2)
        result = utils.wordtoarray(data, 2)
        np.testing.assert_array_equal(expect, result)

    def test_wordtoarray_long_words_get_cut_off(self):
        data = ["abz", "cd"]
        expect = np.array(["a", "b", "c", "d"], dtype="S1").reshape(2, 2)
        result = utils.wordtoarray(data, 2)
        np.testing.assert_array_equal(expect, result)

class TestArraytoWord(unittest.TestCase):
    def test_arraytoword_basic_usage(self):
        data = np.array(["a", "b", "c", "d"], dtype="S1").reshape(2, 2)
        expect = ["ab", "cd"]
        result = utils.arraytoword(data)
        self.assertEqual(expect, result)
    def test_arraytoword_short_words_get_padded(self):
        data = np.array(["a", " ", "c", "d"], dtype="S1").reshape(2, 2)
        expect = ["a ", "cd"]
        result = utils.arraytoword(data)
        self.assertEqual(expect, result)
    def test_arraytoword_strip_excess_from_words(self):
        data = np.array(["a", " ", "c", "d"], dtype="S1").reshape(2, 2)
        expect = ["a", "cd"]
        result = utils.arraytoword(data, strip=True)
        self.assertEqual(expect, result)

