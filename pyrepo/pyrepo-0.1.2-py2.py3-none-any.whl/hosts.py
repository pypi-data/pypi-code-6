# -*- coding: utf-8 -*-
"""
    This module provides the repository Host type and common Host
    objects (github_host, bitbucket_host).
"""

import re

class Host(object):
    """
    Represents a host of repositories and how import_path identifiers of
    repositories are mapped to the host's urls.
    """
    
    def __init__(self, command_name_func=None, **kwargs):
        """
        :param str name: name of the repository host
        :param str prefix: prefix to matching import paths should have
        :param str pattern: regex pattern for the import path
        :param str command_name: name of the command for interacting
            with hosted repositories
        :param func command_name_func: func(`import_path`) which returns
            the str name of a command to be used for the host's 
            `import_path` repository. May raise `ImportPathError`.
            Defaults to None and `command_name` is used directly.
        :param str url_format: format string for the repository url,
            which should contain a `import_path` format specifier.
        :raises: ValueError
        """
        self.name = kwargs["name"]
        self.prefix = kwargs["prefix"]
        self.pattern = re.compile(kwargs["pattern"])
        self.command_name = kwargs["command_name"]
        self.command_name_func = command_name_func
        self.url_format = kwargs["url_format"]
        if self.command_name_func is None and self.command_name is None:
            raise ValueError(("Host {0} `command_name` and" 
                "`command_name_func` cannot both be None")
                .format(self.name))

#: github.com repository host definition
github_host = Host(
    name="Github",
    prefix="github.com/",
    pattern="^(?P<repo_root>github\.com/[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+)(/[A-Za-z0-9_.\-]+)*$",
    command_name="git",
    url_format="https://{import_path}")

#: bitbucket.org repository host definition
bitbucket_host = Host(
    name="Bitbucket",
    prefix="bitbucket.org/",
    pattern="^(?P<repo_root>bitbucket\.org/(?P<bitname>[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+))(/[A-Za-z0-9_.\-]+)*$",
    command_name="git",
    url_format="https://{import_path}")

#: default set of repository hosts
default_hosts = [github_host, bitbucket_host]
