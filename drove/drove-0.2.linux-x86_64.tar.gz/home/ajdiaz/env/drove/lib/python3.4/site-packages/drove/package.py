#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""This module contains definitions and classes to handle
plugin packages. A package is formerly a tarball file
which contains a plugin in the normalize plugin packaging
format.

A plugin package must contain a folder ``plugin``, with the
plugin code inside (which can be a module(s) or other
package(s).
"""

import os
import glob
import shutil
import tarfile

from six.moves import urllib

from .util import temp
from .util import tester


class PackageError(Exception):
    """Models an error related with a malformed package"""


class Package(object):

    @staticmethod
    def _get_candidates(dir):
        """Given a directory, find plugin candidates, which are
        folders that match the expression *author*-*plugin*-*version*.
        """
        candidates = glob.glob(os.path.join(dir, "*-*-*"))

        for candidate in candidates:
            if os.path.isdir(candidate):
                items = os.path.split(candidate.strip())[-1].split("-")
                yield items[0], "-".join(items[1:-1]), items[-1]

    @staticmethod
    def _run_tests(path):
        """Run tests with uniitest if exist.

        :type path: str
        :param path: the top path to search tests.
        """
        for result in tester.run_tests(path):
            if not result.wasSuccessful():
                for fail in result.failures:
                    raise PackageError("Test failure: %s" % (fail[1],))

    @staticmethod
    def _init_package(dir_path, version=None):
        """Initialize a package in specified path. This function
        create the ``__init__.py`` file or update it if exists.

        :type dir_path: str
        :param dir_path: The path to initialize as python package

        :type version: str
        :param version: The version of the package. If exists create
            ``__version__`` variable into ``__init__.py`` file.
        """
        if not os.path.exists(dir_path):
            os.mkdir(dir_path, 0o755)
        elif not os.path.isdir(dir_path):
            raise PackageError("path '%s' is not a directory" % (dir_path,))
        if version is None:
            open(os.path.join(dir_path, "__init__.py"), 'a').close()
        else:
            with open(os.path.join(dir_path, "__init__.py"), 'a') as f:
                f.write("__version__ = '%s'\n" % (version,))

    @staticmethod
    def _install_requirements(path):
        """Resolve and install requirements. This function will read
        the file ``requirements.txt`` from path passed as argument, and
        then use pip to install them.
        """
        requirements = os.path.join(path, "requirements.txt")
        if os.path.exists(requirements):
            try:
                from pip import main as pip_main
            except ImportError:
                raise PackageError("This module needs python dependencies. " +
                                   "You need pip to install dependencies, " +
                                   "please install pip libraries before.")

            pip_main(["-q", "install", "-r", requirements])

    @classmethod
    def from_url(kls, url, plugin_dir, upgrade=False):
        with urllib.request.urlopen(url) as response:
            return kls.from_tarballfd(response, plugin_dir, upgrade)

    @classmethod
    def from_installed(kls, author, plugin, plugin_dir):
        for dir in plugin_dir:
            dir = os.path.join(os.path.expanduser(dir), author, plugin)
            if os.path.isdir(dir):
                # XXX We need to get version from __init__.py
                return Package(author, plugin, None, [dir])

    @classmethod
    def from_tarballfd(kls, fd, plugin_dir, upgrade=False):
        with temp.directory() as tmp_dir:
            with tarfile.open(mode="r:gz", fileobj=fd) as tarball:
                tarball.extractall(path=tmp_dir)

            candidates = [x for x in Package._get_candidates(tmp_dir)]

            if len(candidates) < 1:
                raise PackageError("Package dot not contains packages" +
                                   "inside.")
            if len(candidates) > 1:
                raise PackageError("Package contains more than " +
                                   "one package inside.")

            author, plugin, version = candidates[0]
            package = Package(author, plugin, version)

            if package.is_installed(plugin_dir) and not upgrade:
                raise PackageError("Package '%s.%s' already installed"
                                   % (author, plugin,))

            plugin_path = os.path.join(
                tmp_dir, "%s-%s-%s" % (author, plugin, version,)
            )

            local_plugin = os.path.join(plugin_path, "plugin")

            if not os.path.isdir(local_plugin):
                raise PackageError("Package does not contain any plugin")

            Package._run_tests(plugin_path)

            for dir in plugin_dir:
                dest_dir = os.path.join(dir, author, plugin)
                Package._install_requirements(plugin_path)
                Package._init_package(os.path.join(dir, author))
                shutil.copytree(local_plugin, dest_dir)
                Package._init_package(dest_dir, version)
                package.install_dir.append(dest_dir)

        return package

    @classmethod
    def from_tarball(kls, tarball, plugin_dir, upgrade=False):
        """Create a new package from tarball file

        :type tarball: str
        :param tarball: the filename of the tarball with the plugin

        :type plugin_dir: list of str
        :param plugin_dir: a list of path to install the tarball

        :type upgrade: bool
        :param upgrade: if true, upgrade the package, otherwise failed
            if package is already installed.
        """
        with open(tarball, 'rb') as f:
            return kls.from_tarballfd(f, plugin_dir, upgrade)

    def __init__(self, author, plugin, version, install_dir=[]):
        self.author = author
        self.plugin = plugin
        self.version = version
        self.install_dir = install_dir
        self.name = "%s.%s" % (author, plugin)

    def is_installed(self, dirs):
        """Return true if the package is installed in any directory of the
        dirs list passed as argument.
        """
        for dir in dirs:
            if os.path.isdir(os.path.join(dir, self.author, self.plugin)):
                return True
        return False

    def remove(self):
        for dir in self.install_dir:
            shutil.rmtree(dir, ignore_errors=True)
            parent = os.sep.join(os.path.abspath(dir).split(os.sep)[:-1])
            if os.path.isdir(parent) and \
               not [x for x in os.listdir(parent) if x[0] != "_"]:
                shutil.rmtree(parent)
