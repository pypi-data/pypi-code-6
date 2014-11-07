#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from . import Command
from . import CommandError
from ..package import Package


class RemoveCommand(Command):
    """Remove an installed plugin"""
    def execute(self):
        plugin = self.args.plugin
        install_global = self.args.install_global

        if "." not in plugin:
            raise CommandError("plugin must contain almost author.plugin")

        plugin_dir = self.config.get("plugin_dir", None)

        if not plugin_dir or len(plugin_dir) == 0:
            raise CommandError("Missing plugin_dir in configuration")

        if install_global:
            plugin_dir = plugin_dir[-1]
        else:
            plugin_dir = plugin_dir[0]

        author, plugin = plugin.split(".", 1)

        package = Package.from_installed(author, plugin, [plugin_dir])
        package.remove()
