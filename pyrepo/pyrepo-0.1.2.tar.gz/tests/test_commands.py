#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Command tests
"""

import unittest
import shutil
import tempfile
import subprocess
import os

from pyrepo import git_command, hg_command
from utils import MockSourceRepo

class CommandTestBase():
    """
    Common tests and setUp/tearDown for the `Command` class. 
    Structured like a unittest.TestCase, but this class is not a true
    TestCase, it will not be run. Create a TestCase that also inherits
    from this type to perform any Command testing.

    Requirements to use this base:
    * TestCase implementation must implement `get_command`.
    """

    def get_command(self):
        """Returns a Command to be tested."""
        raise NotImplementedError(
            "TestCases inheriting from CommandTestBase must implement.")

    def command_user_setup(self):
        """
        Return a function that sets up the command user following 
        init.
        """
        raise NotImplementedError(
            "TestCases inheriting from CommandTestBase must implement.")

    def setUp(self):
        """
        Setup a temporary repository directory and directory to clone 
        into. Ensure tearDown removes these directories.
        """
        self.command = self.get_command()
        self.command_user_setup = self.command_user_setup()
        self.repo_dir = tempfile.mkdtemp()    # repo on local filesystem
        self.mock_repo = MockSourceRepo(
            self.command, 
            self.repo_dir,
            command_user_setup=self.command_user_setup)
        self.target_dir = tempfile.mkdtemp()  # clone/create into this dir

    def tearDown(self):
        """Teardown after each test"""
        shutil.rmtree(self.repo_dir)
        shutil.rmtree(self.target_dir)

    def test_clone(self):
        self.command.clone(self.repo_dir, self.target_dir)
        target_test_path = self.mock_repo.test_path(self.target_dir)
        self.assertTrue(os.path.isfile(target_test_path))
        with open(target_test_path) as f:
            self.assertTrue('Version 1' in f.read())

    # TODO: test update once sync to commit implemented
    # TODO: test does not perform non-ff updates

    def test_update_already_updated(self):
        self.command.clone(self.repo_dir, self.target_dir)
        (stdout, stderr) = self.command.update(self.target_dir)
        up_to_date = 'Already up-to-date.' in stdout.decode('utf-8')
        no_changes = 'no changes found' in stdout.decode('utf-8')
        self.assertTrue(up_to_date or no_changes)

    # def test_tags(self):
    #     self.command.clone(self.repo_dir, self.target)
    #     tags = self.command.tag_list(cwd=self.target)
    #     expected_tags = ["master", "v0.0.2", "v0.0.3"]
    #     self.assertEqual(set(expected_tags), set(tags))


class GitCommandTestCase(CommandTestBase, unittest.TestCase):

    def get_command(self):
        return git_command

    def command_user_setup(self):
        def git_user_setup(directory):
            subprocess.Popen(
                "git config user.name 'Pyrepo Tester'".split(),
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                cwd=directory).communicate()
            subprocess.Popen(
                "git config user.email 'test@test.com'".split(),
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                cwd=directory).communicate()
        return git_user_setup


class HgCommandTestCase(CommandTestBase, unittest.TestCase):

    def get_command(self):
        return hg_command

    def command_user_setup(self):
        def hg_user_setup(directory):
            # TODO: mutates Mercurial env of user running the test :(
            os.environ['HGUSER'] = 'Pyrepo Tester'
        return hg_user_setup


if __name__ == '__main__':
    unittest.main()
