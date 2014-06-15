#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Utilities to aid in testing.
"""

import subprocess
import os

class MockSourceRepo(object):
    """
    Represents a source repository on the local filesystem for mocking
    purposes. The repository is setup to have some history and tags.
    """

    def __init__(self, command, directory, command_user_setup=None, 
        repo_file='TESTFILE.txt'):
        self.command = command        # command corresponding to the repo
        self.directory = directory    # location of the mock repo
        self.repo_file = repo_file    # name of the file in the repo
        # a function that sets up the command's user, following init
        self.command_user_setup = command_user_setup
        self._setup()

    def test_path(self, clone_directory=None):
        """
        Returns the path to the file in the MockSourceRepo that is used
        for testing.
        :param str clone_directory: Optional path to a directory clone 
        of the MockSourceRepo
        :returns: path to the file in the mock repo that is used for
        testing. If a `clone_directory` was given, returns that path to
        the file used for testing within the cloned mock repo.
        """
        if clone_directory is None:
            return os.path.join(self.directory, self.repo_file)
        return os.path.join(clone_directory, self.repo_file)

    def _setup(self):
        self._initialize_repo()
        self._write_file('Version 0')
        self._snapshot('commit-0')
        self._write_file('Version 1')
        self._snapshot('commit-1')

    def _initialize_repo(self):
        """Initializes a local mock repository."""
        self.command.init(self.directory)
        if self.command_user_setup is not None:
            self.command_user_setup(self.directory)

    def _write_file(self, test_text):
        """
        Adds the given test_text to the mock repository's repo_file.
        """
        with open(self.test_path(), 'w') as f:
            f.write(test_text)

    def _snapshot(self, message):
        """
        Snapshot the mock repository state (i.e. command should add the
        file in some way and commit it (implementation depends on 
        command)
        :param str message: snapshot/commit message
        """
        # TODO: remove limitation that commit should be 1 word
        self.command.add(self.repo_file, dir=self.directory)
        self.command.commit(message, dir=self.directory)
