# coding: utf-8
from src.parse_tools import list_directory_files
from src.parse_tools import get_node_match
import re
import unittest
import os

class ParserTest(unittest.TestCase):

    def setUp(self):
        self.foo_c = "test_data/dummy_directory/foo.c"
        self.foo_cs = "test_data/dummy_directory/foo.cs"
        self.dummy_lst = sorted([self.foo_c, self.foo_cs])
        self.bar_c = "test_data/dummy_directory/dummy_child/bar.c"
        self.bar_cs = "test_data/dummy_directory/dummy_child/bar.cs"
        self.dummy_child_lst = sorted([self.bar_c, self.bar_cs])

        self.dummy_dir = "test_data/dummy_directory"
        self.dummy_child = "src/test_data/dummy_directory/dummy_child"


    def list_abs_path(self, lst):
        return sorted(map(lambda fn: os.path.abspath(fn), lst))

    def test_listdir_no_recurse(self):
        result_lst = list_directory_files(self.dummy_dir, False, '*')
        self.assertEqual(sorted(result_lst), sorted(self.dummy_lst))

    def test_listdir_recurse(self):
        result_lst = sorted(list_directory_files(self.dummy_dir, True, '*'))
        self.assertEqual(result_lst, sorted(self.dummy_lst+self.dummy_child_lst))

    def test_get_node_match(self):
        test_iterable = ["match", "asdf asdf"]
        test_node = {'depth': 0, 'initial': lambda text: re.search('match', text) or None}
        result_match = get_node_match(test_node, test_iterable[0], test_iterable, False)
        return self.assertEqual(result_match.string, "match")


if __name__ == '__main__':
    unittest.main()











