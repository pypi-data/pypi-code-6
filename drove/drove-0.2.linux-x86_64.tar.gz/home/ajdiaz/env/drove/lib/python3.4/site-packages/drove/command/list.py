#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import os
from . import Command
from . import CommandError


class ListCommand(Command):
    """List installed plugins"""
    def execute(self):
        plugin_dir = self.config.get("plugin_dir", None)
        if not plugin_dir:
            raise CommandError("Missing plugin_dir in configuration")
        for dirname in plugin_dir:
            for author_name in os.listdir(os.path.expanduser(dirname)):
                author_dname = os.path.join(dirname, author_name)
                if author_name[0] != "_" and os.path.isdir(author_dname):
                    for plugin_name in os.listdir(author_dname):
                        plugin_dname = os.path.join(author_dname, plugin_name)
                        if plugin_name[0] != "_" and \
                           os.path.isdir(plugin_dname):
                            self.log.info("%s.%s" % (author_name,
                                                     plugin_name,))
