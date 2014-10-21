# -*- coding: utf-8 -*-
'''
Created on 8 Jan 2011

@author: G.Bronzini
'''

#from django.test import TestCase
from wizdict import group_dict, get_dicts, group_list, analyze_dict_list
from unittest import TestCase



class DictUtilsTestCase(TestCase):
    def test_group_dict(self):
        self.assertEqual(group_dict([{'A': 1, 'B': 2, 'C': 3}, {'A': 1, 'C': 33}, {'A': 22, 'B': 2, 'C': None}], 'A'),
                         {1: [{'A': 1, 'B': 2, 'C': 3}, {'A': 1, 'C': 33}], 22: [{'A': 22, 'B': 2, 'C': None}]})

        self.assertEqual(group_dict([{'A': 1, 'B': 2, 'C': 3}, {'A': 1, 'C': 33}, {'A': 22, 'B': 2, 'C': None}], 'B'),
                         {2: [{'A': 1, 'B': 2, 'C': 3}, {'A': 22, 'B': 2, 'C': None}], '_nokey_': [{'A': 1, 'C': 33}]})

        self.assertEqual(group_dict([{'A': 1, 'B': 2, 'C': 3}, {'A': 1, 'C': 33}, {'A': 22, 'B': 2, 'C': None}], 'C'),
                         {None: [{'A': 22, 'B': 2, 'C': None}], 3: [{'A': 1, 'B': 2, 'C': 3}], 33: [{'A': 1, 'C': 33}]})

    def test_group_dict_advanced(self):
        self.assertEqual(group_dict([{'A': 1, 'B': 2, 'C': 3}, {'A': 1, 'C': 33}, {'A': 22, 'B': 2, 'C': None}],
                                    lambda d: 0 if not ('B' in d) else d['B']),
                         {0: [{'A': 1, 'C': 33}], 2: [{'A': 1, 'C': 3, 'B': 2}, {'A': 22, 'C': None, 'B': 2}]})

        self.assertEqual(group_dict([{'A': 1, 'B': 2, 'C': 3}, {'A': 1, 'C': 33}, {'A': 22, 'B': 2, 'C': None}],
                                    ('A', lambda d: 3 if not d['C'] else d['C'])),
                         {(22, 3): [{'A': 22, 'C': None, 'B': 2}], (1, 3): [{'A': 1, 'C': 3, 'B': 2}],
                          (1, 33): [{'A': 1, 'C': 33}]})

    def test_group_list(self):
        self.assertEqual(group_list([[1, 'B', 'C'], ['A', 2, None], [1, 'C', 33]], 0),
                         {1: [[1, 'B', 'C'], [1, 'C', 33]], 'A': [['A', 2, None]]})

    def test_get_dicts(self):
        self.assertEqual(get_dicts([{'A': 1, 'B': 2, 'C': 3}, {'A': 1, 'C': 33}, {'A': 22, 'B': 2, 'C': None}], A=1),
                         [{'A': 1, 'B': 2, 'C': 3}, {'A': 1, 'C': 33}])

        self.assertEqual(get_dicts([{'A': 1, 'B': 2, 'C': 3}, {'A': 1, 'C': 33}, {'A': 22, 'B': 2, 'C': None}], A=1, C=3),
                         [{'A': 1, 'B': 2, 'C': 3}])

        self.assertEqual(get_dicts([{'A': 1, 'B': 2, 'C': 3}, {'A': 1, 'C': 33}, {'A': 22, 'B': 2, 'C': None}],
                                   lambda d: d['C'] in [None, 33]),
                         [{'A': 1, 'C': 33}, {'A': 22, 'B': 2, 'C': None}])

    def test_analyze_dict_list(self):
        self.assertDictEqual(analyze_dict_list([{'A': 1, 'B': 2, 'C': 3}, {'A': 1, 'C': 33}, {'A': 22, 'B': 2, 'C': None}],
                                 ['A', '-C']),
                          {'C_min': 33, 'C_max': 3, 'C_cnt': 2, 'C_sum': 36, 'C_avg': 18.0, 'C_med': 33,
                           'A_min': 1, 'A_max': 22, 'A_cnt': 3, 'A_sum': 24, 'A_avg': 8.0, 'A_med': 22 } )

        self.assertDictEqual(analyze_dict_list([{'A': 1, 'B': 2, 'C': 3}, {'A': 1, 'C': 33}, {'A': 22, 'B': 2, 'C': None}],
                                 ['A', '-C'], True),
            { 'C': {'C_med': 33, 'C_min': 33, 'C_cnt': 2, 'C_max': 3, 'C_sum': 36, 'C_avg': 18.0},
              'A': {'A_max': 22, 'A_sum': 24, 'A_med': 22, 'A_min': 1, 'A_cnt': 3, 'A_avg': 8.0 } })

        # try:
        #     extract([{'A': 1, 'B': 2, 'C': 3}, {'A': 1, 'C': 33}], lambda x: x['B'])
        #     self.fail("should raise KeyError exception")
        # except KeyError:
        #     pass  # TEST OK
        # except Exception as e:
        #     self.fail("should raise KeyError exception and not %s" % type(e))
        #     self.fail("shouldn't happen")
