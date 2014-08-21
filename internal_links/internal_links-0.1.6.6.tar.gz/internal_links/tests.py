# encoding: utf-8

import unittest
from .helpers import insert_links_to_text, find_text_occurrences


class TestFindText(unittest.TestCase):

    def test_find_text_occurrences(self):
        text_dict = {'content': 'Ok, Ala ma kota, ala kota tez ma, ale ola nie ma kota tak jak ala'}
        self.assertEqual(find_text_occurrences('Ala', text_dict)[0]['word'], 'Ala')


class TestInsertLinks(unittest.TestCase):
    def setUp(self):
        self.result_text = 'Ok, <a href="http://ala.com" alt="Ala" title="Ala">Ala</a> ma kota, ' \
                           '<a href="http://ala.com" alt="Ala" title="Ala">Ala</a> kota tez ma, ale ola nie ma kota ' \
                           'tak jak <a href="http://ala.com" alt="Ala" title="Ala">Ala</a>'

    def test_insert_links_to_text(self):
        text_dict = {'content': 'Ok, Ala ma kota, ala kota tez ma, ale ola nie ma kota tak jak ala',
                     'modified': False}
        matches = [{'word': 'Ala', 'start': 4, 'end': 7},
                   {'word': 'Ala', 'start': 17, 'end': 20},
                   {'word': 'Ala', 'start': 62, 'end': 65}]
        self.assertEqual(insert_links_to_text(text_dict, matches, "http://ala.com")['content'], self.result_text)
        self.assertTrue(insert_links_to_text(text_dict, matches, "http://ala.com")['modified'])
