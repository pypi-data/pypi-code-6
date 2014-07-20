"""
Monkey-patching django.core.management functions
"""

import collections

from django.core import management as core_management
from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.core.management.color import color_style


_commands = None


def get_commands():
    global _commands
    if _commands is None:
        _commands = dict([(name, ['django.core']) for name in \
            core_management.find_commands(core_management.__path__[0])])

        # Find the installed apps
        from django.conf import settings
        try:
            apps = settings.INSTALLED_APPS
        except ImproperlyConfigured:
            # Still useful for commands that do not require functional settings
            # like startproject or help
            apps = []

        # Find and load the management module for each installed app.
        for app_name in apps:
            try:
                path = core_management.find_management_module(app_name)
                for name in core_management.find_commands(path):
                    if name in _commands:
                        _commands[name].append(app_name)
                    else:
                        _commands[name] = [app_name]
            except ImportError:
                pass  # No management module - ignore this app

    core_management._commands = _commands
    return _commands

core_management.get_commands = get_commands


def load_command_class(app_names, name):
    prev_cmd_class = None
    for app in app_names:
        module = core_management.import_module('%s.management.commands.%s' % \
                                               (app, name))
        cmd_class = module.Command
        # fake inheritance by playing with the __bases__ tuple
        if prev_cmd_class:
            bases = list(cmd_class.__bases__)
            # remove from the bases any class from which the previous Command
            # derives
            for b in cmd_class.__bases__:
                if issubclass(prev_cmd_class, b):
                    bases.remove(b)

            # and replace the __bases__ tuple, with the previous Command in
            # first position
            cmd_class.__bases__ = (prev_cmd_class,) + tuple(bases)

            # now deal with the option_list, so that prev_cmd_class' options
            # are not 'forgotten' in cmd_class, and cmd_class' s options are
            # simply added to the command's option_list
            cmd_class.option_list = prev_cmd_class.option_list + \
                tuple(set(cmd_class.option_list). \
                      difference(prev_cmd_class.option_list))

        prev_cmd_class = cmd_class

    return cmd_class()

core_management.load_command_class = load_command_class


def main_help_text(self, commands_only=False):
    if commands_only:
        usage = sorted(get_commands().keys())
    else:
        usage = [
            "",
            "Type '%s help <subcommand>' for help on a specific subcommand." \
                % self.prog_name,
            "",
            "Available subcommands:",
        ]
        commands_dict = collections.defaultdict(lambda: [])
        for name, apps in six.iteritems(get_commands()):
            for app in apps:
                if app == 'django.core':
                    app = 'django'
                else:
                    app = app.rpartition('.')[-1]
                commands_dict[app].append(name)
        style = color_style()
        for app in sorted(commands_dict.keys()):
            usage.append("")
            usage.append(style.NOTICE("[%s]" % app))
            for name in sorted(commands_dict[app]):
                usage.append("    %s" % name)
    return '\n'.join(usage)

core_management.ManagementUtility.main_help_text = main_help_text
