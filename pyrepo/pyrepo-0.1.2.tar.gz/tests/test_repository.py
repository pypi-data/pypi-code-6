#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Repository tests.
"""

import os
import shutil
import tempfile
import unittest
import subprocess

from pyrepo import Repository, ImportPathError
from pyrepo import git_command, hg_command
from pyrepo.repo import RepoImporter
from utils import MockSourceRepo

class InitRepositoryTestCase(unittest.TestCase):

    def test_init_command_and_url(self):
        command = git_command
        url = "https://github.com/dghubble/pyrepo"
        repo = Repository(command=command, url=url)
        self.assertEqual(command.name, repo.command.name)
        self.assertEqual(url, repo.url)
        self.assertEqual(None, repo.import_path)

    def test_init_import_path(self):
        import_path = "github.com/dghubble/pyrepo"
        repo = Repository(import_path=import_path)
        self.assertEqual(git_command.name, repo.command.name)
        expected_url = "https://github.com/dghubble/pyrepo"
        self.assertEqual(expected_url, repo.url)
        self.assertEqual(import_path, repo.import_path)

    def test_init_prefer_command(self):
        """
        When the `import_path` must be resolved, but a command was
        given directly, prefer the command argument to the resolved
        command.
        """
        command = hg_command
        import_path = "github.com/dghubble/pyrepo"
        repo = Repository(command=command, import_path=import_path)
        self.assertEqual(command.name, repo.command.name)

    def test_init_prefer_url(self):
        """
        When the `import_path` must be resolved, but a url was
        given directly, prefer the url argument over the resolved url.
        """
        url = "https://preferred_url"
        import_path = "github.com/dghubble/pyrepo"
        repo = Repository(url=url, import_path=import_path)
        self.assertEqual(url, repo.url)

    def test_init_invalid_import_path(self):
        # general invalid path
        self.assertRaises(ImportPathError, Repository, 
            import_path="://invalid_path")
        # path matches no host start patterns
        self.assertRaises(ImportPathError, Repository, 
            import_path="gggiiitthub.com/")
        # path matches a host's start, but not pattern
        self.assertRaises(ImportPathError, Repository, 
            import_path="github.com/missingproj")
        self.assertRaises(ImportPathError, Repository, 
            import_path="github.com/missingproj/")
        self.assertRaises(ImportPathError, Repository, 
            import_path="bitbucket.org/missingproj")
        self.assertRaises(ImportPathError, Repository, 
            import_path="bitbucket.org/missingproj/")

    def test_init_missing_arguments(self):
        # missing url, missing import_path to resolve url
        self.assertRaises(ValueError, Repository,
            command=git_command)
        # missing command, missing import_path to resolve url
        self.assertRaises(ValueError, Repository,
            url="https://github.com/dghubble/pyrepo")
        # missing arguments for resolving command and url
        self.assertRaises(ValueError, Repository)


class RepositoryTestCase(unittest.TestCase):

    def setUp(self):
        """
        Setup a temporary repository directory and directory to clone 
        into. Ensure tearDown removes these directories.
        """
        # TODO: Hardcoded to Git currently, remove this coupling
        self.repo_dir = tempfile.mkdtemp()    # repo on local filesystem
        self.mock_repo = MockSourceRepo(
            git_command, 
            self.repo_dir,
            command_user_setup=self.command_user_setup())
        self.target_dir = tempfile.mkdtemp()  # clone/create into this dir
        self.repo = Repository(command=git_command, url=self.repo_dir)

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

    def tearDown(self):
        """Teardown after each test"""
        shutil.rmtree(self.repo_dir)
        shutil.rmtree(self.target_dir)

    def test_clone(self):
        self.repo.clone(self.target_dir)
        target_test_path = self.mock_repo.test_path(self.target_dir)
        self.assertTrue(os.path.isfile(target_test_path))
        with open(target_test_path) as f:
            self.assertTrue('Version 1' in f.read())

    def test_update_already_updated(self):
        self.repo.clone(self.target_dir)
        (stdout, stderr) = self.repo.update(self.target_dir)
        up_to_date = 'Already up-to-date.' in stdout.decode('utf-8')
        no_changes = 'no changes found' in stdout.decode('utf-8')
        self.assertTrue(up_to_date or no_changes)


# TODO: test importer with different host and command sets
class RepoImporterTestCase(unittest.TestCase):

    def setUp(self):
        self.importer = RepoImporter()
        pass

    def test_github_import_name(self):
        import_path = "github.com/dghubble/python-role"
        (command, url) = self.importer.resolve(import_path)
        self.assertEqual("git", command.name)
        self.assertEqual("https://github.com/dghubble/python-role", 
            url)

    def test_bitbucket_import_name(self):
        import_path = "bitbucket.org/dghubble/role-template"
        (command, url) = self.importer.resolve(import_path)
        self.assertEqual("git", command.name)
        self.assertEqual("https://bitbucket.org/dghubble/role-template", 
            url)

if __name__ == '__main__':
    unittest.main()
