#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os

from . import Command
from . import CommandError

from ..package import Package


class InstallCommand(Command):

    def execute(self):
        plugin_dir = self.config.get("plugin_dir", None)
        plugin = self.args.plugin
        upgrade = self.args.upgrade
        install_global = self.args.install_global

        if not plugin_dir:
            raise CommandError("'plugin_dir' is not configured")

        if install_global:
            plugin_dir = os.path.expanduser(plugin_dir[-1])
        else:
            plugin_dir = os.path.expanduser(plugin_dir[0])

        # If plugin string is an URL
        if plugin.split("://")[0] in ["http", "https", "ftp"]:
            package = Package.from_url(plugin, [plugin_dir], upgrade)
        # If plugin string is file in the filesystem
        elif os.path.exists(plugin) and os.path.isfile(plugin):
            # If file is a tarball
            if plugin.endswith(".tar.gz"):
                package = Package.from_tarball(plugin, [plugin_dir], upgrade)
            else:
                raise CommandError("Provided package file is not a tarball")
        else:
            raise CommandError("Unknown method to install a package")

        self.log.info("Installed package: %s" % (package.name,))
