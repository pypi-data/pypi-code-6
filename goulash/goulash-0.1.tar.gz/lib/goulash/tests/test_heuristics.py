""" goulash.tests.test_heuristics
"""
import unittest
from goulash import heuristics as hx


class TestHeuristics(unittest.TestCase):

    def test_answer(self):
        self.assertTrue(hx.Answer(42))
        self.assertTrue(hx.Answer(True))
        self.assertFalse(hx.Answer(False))
        self.assertFalse(hx.Answer(0))

    def test_explained_answer(self):
        explanation = 'argument from authority'
        tmp = hx.ExplainedAnswer(True, explanation)
        self.assertTrue(tmp)
        self.assertEqual(tmp.explanation, explanation)
        actual = str(tmp)
        expected = '(ExplainedAnswer: argument from authority)'
        self.assertEqual(actual, expected)

    def test_not_applicable(self):
        tmp = hx.NotApplicable("heuristic does not apply!")
        self.assertFalse(tmp)
        tmp = hx.NotApplicable()
        self.assertFalse(tmp)

    def test_affirmative(self):
        tmp = hx.Affirmative("yup")
        self.assertTrue(tmp)

    def test_negative(self):
        tmp = hx.Negative("nope")
        self.assertFalse(tmp)
