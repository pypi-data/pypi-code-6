import unittest

from subdicts import utils


class TestSubDicts(unittest.TestCase):
    
    def test_parse_given_dictionary_keys(self):
        given = {'firstname': 'arnelle', 'lastname': 'balane'}
        expected = {'firstname': 'arnelle', 'lastname': 'balane'}
        self.assertEqual(expected, utils.parse(given))

    def test_parse_given_simple_nested_dictionary_keys(self):
        given = {'person[firstname]': 'arnelle', 'person[lastname]': 'balane'}
        expected = {'person': {'firstname': 'arnelle', 'lastname': 'balane'}}
        self.assertEqual(expected, utils.parse(given))

    def test_parse_given_deeply_nested_dictionary_keys(self):
        given = {'person[personal_information][name][first]': 'arnelle',
                 'person[personal_information][name][last]': 'balane',
                 'person[personal_information][gender]': 'male',
                 'person[personal_information][email]': 'arnellebalane@gmail.com',
                 'person[address][province]': 'bohol',
                 'person[address][city][name]': 'tagbilaran city',
                 'person[address][city][zip_code]': '6300'}
        expected = {'person': {
                        'personal_information': {
                            'name': {
                                'first': 'arnelle',
                                'last': 'balane'
                            },
                            'gender': 'male',
                            'email': 'arnellebalane@gmail.com'
                        },
                        'address': {
                            'province': 'bohol',
                            'city': {
                                'name': 'tagbilaran city',
                                'zip_code': '6300'
                            }
                        }
                    }}
        self.assertEqual(expected, utils.parse(given))
