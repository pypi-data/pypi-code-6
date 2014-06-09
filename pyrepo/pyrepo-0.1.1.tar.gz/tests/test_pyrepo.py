#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Package tests
"""
import unittest
import shutil
import tempfile
import subprocess
import os
import re

from pyrepo import RepoImporter, Command, Host, git_command

def setupTestGitRepo(directory):
    """
    Setup a testing Git repository with some test commits and tags.
    :param str directory: directory in which a test Git repo should be 
        created
    """
    test_file = 'TESTFILE.txt'
    with open(os.path.join(directory, test_file), 'w') as f:
        f.write('Version 0')
    git_command.init(directory)
    subprocess.Popen(
        "git config user.name 'Tester'".split(),
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        cwd=directory).communicate()
    subprocess.Popen(
        "git config user.email 'test@test.com'".split(),
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        cwd=directory).communicate()
    git_command.add(test_file, dir=directory)
    git_command.commit('Initial', dir=directory)
    with open(os.path.join(directory, test_file), 'w') as f:
        f.write('Version 1')
    git_command.add(test_file, dir=directory)
    git_command.commit('Release', dir=directory)


class GitCommandTestCase(unittest.TestCase):
    """
    Testing environment must have `git` command available.
    """ 

    def setUp(self):
        """
        Setup a temporary Git repository for testing and directory to
        clone/create into. Ensure tearDown removes these directories.
        """
        self.repo_url = tempfile.mkdtemp()
        setupTestGitRepo(self.repo_url)    # make a few test commits
        self.git = git_command
        self.target = tempfile.mkdtemp()   # clone/create into this dir

    def tearDown(self):
        """Teardown after each test"""
        shutil.rmtree(self.repo_url)
        shutil.rmtree(self.target)

    def test_clone(self):
        self.git.clone(self.repo_url, self.target)
        repo_file = os.path.join(self.target, "TESTFILE.txt")
        self.assertTrue(os.path.isfile(repo_file))
        with open(repo_file) as f:
            self.assertTrue('Version 1' in f.read())

    # TODO: test update once sync to commit implemented
    # TODO: test does not perform non-ff updates

    def test_update_already_updated(self):
        self.git.clone(self.repo_url, self.target)
        (stdout, stderr) = self.git.update(self.target)
        self.assertEqual('Already up-to-date.\n', stdout.decode('utf-8'))

    # def test_tags(self):
    #     self.git.clone(self.repo_url, self.target)
    #     tags = self.git.tag_list(cwd=self.target)
    #     expected_tags = ["master", "v0.0.2", "v0.0.3"]
    #     self.assertEqual(set(expected_tags), set(tags))


class RepoImporterTestCase(unittest.TestCase):

    def setUp(self):
        self.importer = RepoImporter()
        pass

    def test_github_import_name(self):
        import_path = "github.com/dghubble/python-role"
        repository = self.importer.resolve(import_path)
        self.assertEqual("git", repository.command.name)
        self.assertEqual("https://github.com/dghubble/python-role", 
            repository.url)

    def test_bitbucket_import_name(self):
        import_path = "bitbucket.org/dghubble/role-template"
        repository = self.importer.resolve(import_path)
        self.assertEqual("git", repository.command.name)
        self.assertEqual("https://bitbucket.org/dghubble/role-template", 
            repository.url)


if __name__ == '__main__':
    unittest.main()





