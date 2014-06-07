# -*- coding: utf-8 -*-
"""
    This module provides a Repository and a RepoImporter. The Repository
    allows managing a general repository via its command. A RepoImporter
    simplifies constructing Repositories from import paths.
"""

from . import hosts
from . import commands
import re

class Repository(object):
    """
    Representation of a repository which is identified by an import_path
    , managed by a :class:`Command <commands.Command>` object, and 
    hosted at some url.
    """

    def __init__(self, identifier, url, command):
        """
        :param str identifier: import path identifying a repository
        :param str url: url from which the repo can be fetched
        :param command: :class:`Command <commands.Command>` for managing 
            the repo
        """
        self.identifier = identifier
        self.url = url
        self.command = command

    def clone(self, *args, **kwargs):
        """
        Arguments are the same as :class:`Command.clone 
        <commands.Command.clone>` arguments.
        """
        return self.command.create(*args, **kwargs)

    def update(self, *args, **kwargs):
        """
        Arguments are the same as :class:`Command.update 
        <commands.Command.update>` arguments.
        """
        return self.command.update(*args, **kwargs)

    def tag_list(self, *args, **kwargs):
        """
        Arguments are the same as :class:`Command.tag_list 
        <commands.Command.tag_list>` arguments.
        """
        return self.command.tag_list(*args, **kwargs)

    def ping(self, *args, **kwargs):
        """
        Arguments are the same as :class:`Command.ping 
        <commands.Command.ping>` arguments.
        """
        return self.command.ping(*args, **kwargs)


class RepoImporter(object):
    """
    Utility for resolving an import path to a :class:`Repository 
    <Repository>` object by determining the repository host, the 
    repository command, the scheme of the repository, and with that
    information, the remote url.

    Usage::

        importer = RepoImporter()
        repo = importer.repo("github.com/dghubble/pyrepo")
        repo.clone()
    """
    DEFAULT_HOSTS = hosts.default_hosts
    DEFAULT_COMMANDS = commands.default_commands

    def __init__(self, hosts=None, commands=None):
        """
        :param list hosts: list of :class:`Host <hosts.Host>` objects 
            to compare import paths against. Defaults
            to :attr:`default_hosts <hosts.default_hosts>`.
        :param list commands: list of :class:`Command 
            <commands.Command>` objects to consider. Defaults to
            :attr:`default_commands <commands.default_commands>`.
        """
        if hosts is None:
            hosts = RepoImporter.DEFAULT_HOSTS
        if commands is None:
            commands = RepoImporter.DEFAULT_COMMANDS
        self.hosts = hosts
        self.commands = commands
    
    def resolve(self, import_path):
        """
        Resolves an import path to a :class:`Repository 
        <Repository>`.

        :param str import_path: import path identifying a repository.
        :returns: :class:`Repository <Repository>` corresponding to the 
            import path 
        :raises: :class:`ImportPathError <ImportPathError>`
        """
        self._validate_import_path(import_path)
        host = self._match_host(import_path)
        command_name = self._match_command(import_path, host)
        # first match or default value if no matches
        command = next((c for c in self.commands if c.name==command_name), 
                       None)
        if command is None:
            raise ImportPathError("{0} is not a valid {1} repository command."
                .format(command_name, host.name))
        # TODO: start respecting per-host scheme
        url = self._build_url(import_path, host, None)
        return Repository(identifier=import_path, url=url, command=command)

    def _validate_import_path(self, import_path):
        if "://" in import_path:
            raise ImportPathError("{0} is not a valid import string."
                .format(import_path))

    def _match_host(self, import_path):
        """
        Checks the import_path against hosts by matching starting
        characters against the host's `prefix` and matching the full 
        import_path against the host's `pattern`.

        :param str import_path: import path identifying a repository
        :returns: matching :class:`Host <hosts.Host>`
        :raises: :class:`ImportPathError <ImportPathError>`
        """
        for host in self.hosts:
            if not import_path.startswith(host.prefix):
                continue
            match = re.search(host.pattern, import_path)
            if match is None:
                if host.prefix == "":
                    # host matches import paths solely by pattern. Continue
                    # to try other hosts.
                    continue
                raise ImportPathError("invalid {0} import path {1}."
                    .format(host.name, import_path))
            return host
        raise ImportPathError("{0} does not match any hosts."
            .format(import_path))

    def _match_command(self, import_path, host):
        """
        Determines the name of the command that should be used to 
        interact with the `host`'s `import_path` repository. Simple 
        hosts have a `command_name` that should be used (e..g. Github -> 
        git). More complex hosts call `command_name_func` to determine
        the command name to use for the repository.

        :param str import_path: import path identifying a repository
        :param host: :class:`Host <hosts.Host>` of the repository, based 
            on the `import_path`
        :returns: `name` of the :class:`Command <commands.Command>` for 
            interacting with the repository
        :raises: :class:`ImportPathError <ImportPathError>`
        """
        if host.command_name_func is None:
            # host repositories all accessed with the same command
            return host.command_name
        else:
            return host.command_name_func(import_path)

    def _build_url(self, import_path, host, scheme):
        """
        Constructs the url from which the `import_path` repository can
        be fetched.

        :param str import_path: import path identifying a repository
        :param host: :class:`Host <hosts.Host>` of the repository, based 
            on the `import_path`
        :param str scheme: url scheme of the repository
        """
        return host.url_format.format(**{"import_path": import_path})


class ImportPathError(Exception):
    """
    Raised when a :class:`RepoImporter <RepoImporter>` cannot create a 
    :class:`Repository <Repository>` object from an import path.
    """
    pass







