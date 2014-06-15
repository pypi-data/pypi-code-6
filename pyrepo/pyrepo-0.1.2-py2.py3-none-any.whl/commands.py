# -*- coding: utf-8 -*-
"""
    This module provides Command, the representation of binary commands 
    used to fetch and manage repositories.
"""

import subprocess
import re


class TagCommand(object):
    """
    Represents a command to list tags to sync onto.
    """

    def __init__(self, cmd, pattern):
        """
        :param cmd: command to list tags
        :param pattern: regex to extract tags
        """
        self.cmd = cmd
        self.pattern = pattern


class Command(object):
    """
    Represents a repository management command (e.g. Git, Mercurial) and 
    its usage.
    """

    def __init__(self, **kwargs):
        """
        Make a repository management command.

        :param str name: executable binary command name (e.g. 'hg')
        :param str long_name: long command name (e.g. 'Mercurial')
        :param str init_cmd: command to initialize a repository
        :param str add_cmd: command to add a {path} to staging
        :param str commit_cmd: commit a changeset to the repo with a
            commit {message}
        :param str create_cmd: command to clone a fresh repository copy
            from {repo_url} to {target_path}
        :param str update_cmd: command to download updates into existing 
            repository
        :param TagCommand tag_list_cmd: command to 
            list repository tags
        :param str tag_sync_cmd: command to sync to a specific tag
        :param str tag_sync_default_cmd: command to sync to the default 
            tag
        :param list schemes: scheme names
        :param str ping_cmd: command to ping for scheme
        """
        self.name = kwargs["name"]
        self.long_name = kwargs["long_name"]
        self.init_cmd = kwargs["init_cmd"]
        self.add_cmd = kwargs["add_cmd"]
        self.commit_cmd = kwargs["commit_cmd"]
        self.create_cmd = kwargs["create_cmd"]
        self.update_cmd = kwargs["update_cmd"]
        self.tag_list_cmd = kwargs["tag_list_cmd"]
        self.tag_sync_cmd = kwargs["tag_sync_cmd"]
        self.tag_sync_default_cmd = kwargs["tag_sync_cmd"]
        self.schemes = kwargs["schemes"]
        self.ping_cmd = kwargs["ping_cmd"]

    def _run(self, cmdline, keyvals, cwd=None):
        """
        Runs the version control system binary with the `cmdline`
        command, interpolated with named `keyvals` dict.
        :params cmdline: command to be executed, e.g. "clone {r} {t}"
        :params keyvals: key-values for interpolation, e.g. 
        {"r": "repourl", "t": "/tmp"}
        :params cwd: directory to execute from, defaults to current dir
        :returns: (standard_out, standard_error)
        """
        cmdline = cmdline.format(**keyvals)
        # 0th argument should always be the name of the binary to execute
        args = [self.name] + cmdline.split()
        return subprocess.Popen(
            args, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            cwd=cwd).communicate()

    def init(self, dir=None):
        """
        Initializes a repository in the given directory.
        """
        return self._run(self.init_cmd, {}, dir)

    def add(self, path, dir=None):
        return self._run(self.add_cmd, {"path": path}, dir)

    def commit(self, message, dir=None):
        return self._run(self.commit_cmd, {"message": message}, dir)

    def clone(self, repo_url, target_path):
        """
        Runs the command to clone/create a new repository.
        :params repi_url: url to remote repo or path to local repo
        :params target: path to intended destination for repo
        """
        return self._run(
            self.create_cmd, 
            {"repo_url": repo_url, 
             "target_path": target_path})

    def update(self, dir=None):
        """
        Runs the command to update a repo, from the given `cwd`
        directory
        """
        return self._run(self.update_cmd, {}, dir)

    def tag_list(self, cwd=None):
        """
        Runs the command to list tags, from the given `cwd` directory.
        """
        (stdout, stderr) = self._run(self.tag_list_cmd.cmd, {}, cwd)
        tags = []
        for line in stdout.decode().split("\n"):
            match = re.search(self.tag_list_cmd.pattern, line)
            if match:
                group_dict = match.groupdict()
                tag = group_dict["tag"]
                if tag is not None: 
                    tags.append(tag)
        return tags
            
    def ping(self, scheme, repo, cwd="."):
        """
        ping
        """
        return self._run(self.ping_cmd, {"scheme": scheme, "repo": repo}, cwd)

#: Git command definition
git_command = Command(
    name="git",
    long_name="Git",
    init_cmd="init",
    add_cmd="add {path}",
    commit_cmd="commit -m '{message}'",
    create_cmd="clone {repo_url} {target_path}",
    update_cmd="pull --ff-only",
    tag_list_cmd=TagCommand("show-ref", 
                        re.compile('(?:tags|origin)/(?P<tag>\S+)$')),
    tag_sync_cmd="checkout {tag}",
    tag_sync_default_cmd="checkout master",
    schemes=["git", "https", "http", "git+ssh"],
    ping_cmd="ls-remote {scheme}://{repo_root}")

# TODO: support branch tag names

#: Mercurial command definition
hg_command = Command(
    name="hg",
    long_name="Mercurial",
    init_cmd="init",
    add_cmd="add {path}",
    commit_cmd="commit -m {message}",
    create_cmd="clone {repo_url} {target_path}",
    update_cmd="pull",
    tag_list_cmd=TagCommand("tags", re.compile('^(\S+)')),
    tag_lookup_cmd="?",
    tag_sync_cmd="update -r {tag}",
    tag_sync_default_cmd="update default",
    schemes=['https', 'http', 'ssh'],
    ping_cmd="identify {scheme}://{repo_root}")

#: default set of commands for repositories
default_commands = [git_command, hg_command]

