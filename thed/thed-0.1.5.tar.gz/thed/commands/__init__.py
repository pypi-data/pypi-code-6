from __future__ import unicode_literals

from . import scaffolds


def add_commands(group):
    group.add_command(scaffolds.group)
