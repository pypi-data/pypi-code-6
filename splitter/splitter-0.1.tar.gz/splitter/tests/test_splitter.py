# -*- coding: utf-8 -*-

"""
test_splitter
----------------------------------

Tests for `splitter` module.
"""
import os
import tempfile

from splitter import splitter

from splitter.tests import base


class TestTokenize(base.TestCase):

    def test_tokenize(self):
        s = "Hello World.\n"
        self.assertEqual(splitter._tokenize(s), ["Hello ", "World.\n"])

    def test_tokenize_leading_whitespace(self):
        s = "\n\nHello World.\n"
        self.assertEqual(splitter._tokenize(s), ["\n\nHello ", "World.\n"])
        self.assertEqual(s, ''.join(splitter._tokenize(s)))

    def test_tokenize_no_trailing_whitespace(self):
        s = "\n\nHello World"
        self.assertEqual(splitter._tokenize(s), ["\n\nHello ", "World"])
        self.assertEqual(s, ''.join(splitter._tokenize(s)))

    def test_sent_tokenize(self):
        s = ("The mobile home owner often invests in site-specific improvements such as a "
             "driveway, steps, walkways, porches, or landscaping. When the mobile home owner "
             "wishes to move, the mobile home is usually sold in place, and the purchaser "
             "continues to rent the pad on which the mobile home is located.")
        s1 = ("The mobile home owner often invests in site-specific improvements such as a "
              "driveway, steps, walkways, porches, or landscaping. ")
        s2 = ("When the mobile home owner wishes to move, the mobile home is usually sold in "
              "place, and the purchaser continues to rent the pad on which the mobile home is "
              "located.")
        self.assertEqual(splitter._sent_tokenize(s), [s1, s2])


class TestSplitter(base.TestCase):

    test_filename_fra = os.path.join(os.path.dirname(__file__), 'text-french.txt')
    test_filename_eng = os.path.join(os.path.dirname(__file__), 'text-english.txt')

    def test_split_simple(self):
        filename = self.test_filename_fra
        n_words = 1000
        chunks = splitter._split(open(filename).read(), n_words)
        for chunk in chunks[:-1]:
            self.assertEqual(len(splitter._tokenize(chunk)), n_words)
        self.assertEqual(len(chunks), 16)

    def test_splitter_exact(self):
        # first sentence is 18 words long
        n_words = 20
        s = ("The mobile home owner often invests in site-specific improvements such as a "
             "driveway, steps, walkways, porches, or landscaping. When the mobile home owner "
             "wishes to move, the mobile home is usually sold in place, and the purchaser "
             "continues to rent the pad on which the mobile home is located.\n")
        chunks = splitter._split(s, n_words)
        for chunk in chunks[:-1]:
            self.assertEqual(len(splitter._tokenize(chunk)), n_words)
        self.assertEqual(len(chunks), 3)
        self.assertTrue(chunks[0].startswith("The mobile home"))
        self.assertTrue(chunks[-1].endswith("is located.\n"))
        self.assertEqual(s, ''.join(chunks))

    def test_splitter_french(self):
        filename = self.test_filename_fra
        output_dir = tempfile.mkdtemp()
        n_words = 1000
        preserve_sentences = False
        splitter.splitter(filename, output_dir, n_words, preserve_sentences)
        self.assertEqual(len(os.listdir(output_dir)), 16)
        chunks = []
        for fn in sorted(os.listdir(output_dir)):
            chunks.append(open(os.path.join(output_dir, fn)).read())
        self.assertEqual(open(filename, 'r').read(), ''.join(chunks))

    def test_splitter_english(self):
        filename = self.test_filename_eng
        output_dir = tempfile.mkdtemp()
        n_words = 1000
        preserve_sentences = False
        splitter.splitter(filename, output_dir, n_words, preserve_sentences)
        self.assertEqual(len(os.listdir(output_dir)), 6)
        chunks = []
        for fn in sorted(os.listdir(output_dir)):
            chunks.append(open(os.path.join(output_dir, fn)).read())
        self.assertEqual(open(filename, 'r').read(), ''.join(chunks))

    def test_split_simple_preserve_sentences(self):
        filename = self.test_filename_fra
        n_words = 1000
        chunks = splitter._split_preserve_sentences(open(filename).read(), n_words)
        self.assertEqual(len(chunks), 16)

    def test_splitter_exact_preserve_sentences(self):
        # first sentence is 18 words long
        # second sentence is 31 words long
        n_words = 35
        s = ("The mobile home owner often invests in site-specific improvements such as a "
             "driveway, steps, walkways, porches, or landscaping. When the mobile home owner "
             "wishes to move, the mobile home is usually sold in place, and the purchaser "
             "continues to rent the pad on which the mobile home is located.\n")
        chunks = splitter._split_preserve_sentences(s, n_words)
        self.assertEqual(len(chunks), 2)
        self.assertTrue(chunks[0].startswith("The mobile home"))
        self.assertTrue(chunks[0].endswith("landscaping. "))
        self.assertTrue(chunks[-1].endswith("is located.\n"))
        self.assertEqual(s, ''.join(chunks))

    def test_splitter_french_preserve_sentences(self):
        filename = self.test_filename_fra
        output_dir = tempfile.mkdtemp()
        n_words = 1000
        preserve_sentences = True
        splitter.splitter(filename, output_dir, n_words, preserve_sentences)
        self.assertEqual(len(os.listdir(output_dir)), 16)
        chunks = []
        for fn in sorted(os.listdir(output_dir)):
            chunks.append(open(os.path.join(output_dir, fn)).read())
        self.assertEqual(open(filename, 'r').read(), ''.join(chunks))

    def test_splitter_english_preserve_sentences(self):
        filename = self.test_filename_eng
        output_dir = tempfile.mkdtemp()
        n_words = 1000
        preserve_sentences = True
        splitter.splitter(filename, output_dir, n_words, preserve_sentences)
        self.assertEqual(len(os.listdir(output_dir)), 6)
        chunks = []
        for fn in sorted(os.listdir(output_dir)):
            chunks.append(open(os.path.join(output_dir, fn)).read())
        self.assertEqual(open(filename, 'r').read(), ''.join(chunks))
