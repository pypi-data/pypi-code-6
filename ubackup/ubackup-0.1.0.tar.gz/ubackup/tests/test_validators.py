import unittest
import click
import os
from uuid import uuid4
from ubackup.cli.validators import directory, mysql_databases


class ValidatorsTest(unittest.TestCase):

    def test_directory_success(self):
        tmp_dir = uuid4().hex
        os.mkdir(tmp_dir)
        tmp_dir = os.path.abspath(tmp_dir)
        directory(None, 'path', tmp_dir)
        os.rmdir(tmp_dir)

    def test_directory_fail(self):
        self.assertRaises(click.BadParameter, directory, None, 'path', uuid4().hex)

    def test_mysql_databases_success(self):
        self.assertEqual(mysql_databases(None, 'databases', '*'), [])
        self.assertEqual(mysql_databases(None, 'databases', 'foo'), ['foo'])
        self.assertEqual(mysql_databases(None, 'databases', 'foo,bar'), ['foo', 'bar'])
        self.assertEqual(mysql_databases(None, 'databases', 'foo bar'), ['foo', 'bar'])
        self.assertEqual(mysql_databases(None, 'databases', 'foo/bar'), ['foo', 'bar'])

    def test_mysql_databases_fail(self):
        self.assertRaises(click.BadParameter, mysql_databases, None, 'databases', ',')
