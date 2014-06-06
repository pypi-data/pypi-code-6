# This file is part of Ubuntu Continuous Integration virtual machine tools.
#
# Copyright 2014 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import re
import sys


from uciconfig import (
    errors as config_errors,
    registries,
)
from ucivms import (
    config,
    errors,
    vms,
)


# The available vm backends are registered here to ensure the config registry
# is loaded before we try to use it.
config.vm_class_registry.register('kvm', vms.Kvm,
                                  'Kernel-based virtual machine')
config.vm_class_registry.register('lxc', vms.Lxc,
                                  'Linux container virtual machine')


class ArgParser(argparse.ArgumentParser):
    """A parser for the uci-vms script."""

    def __init__(self, name, description):
        super(ArgParser, self).__init__(prog='uci-vms {}'.format(name),
                                        description=description)

    def parse_args(self, args=None, out=None, err=None):
        """Parse arguments, overridding stdout/stderr if provided.

        Overridding stdout/stderr is provided for tests.

        :params args: Defaults to sys.argv[1:].

        :param out: Defaults to sys.stdout.

        :param err: Defaults to sys.stderr.
        """
        out_orig = sys.stdout
        err_orig = sys.stderr
        try:
            if out is not None:
                sys.stdout = out
            if err is not None:
                sys.stderr = err
            return super(ArgParser, self).parse_args(args)
        finally:
            sys.stdout = out_orig
            sys.stderr = err_orig

    def parse_known_args(self, args=None, out=None, err=None):
        """Parse known arguments, overridding stdout/stderr if provided.

        Overridding stdout/stderr is provided for tests.

        :params args: Defaults to sys.argv[1:].

        :param out: Defaults to sys.stdout.

        :param err: Defaults to sys.stderr.
        """
        out_orig = sys.stdout
        err_orig = sys.stderr
        try:
            if out is not None:
                sys.stdout = out
            if err is not None:
                sys.stderr = err
            return super(ArgParser, self).parse_known_args(args)
        finally:
            sys.stdout = out_orig
            sys.stderr = err_orig


class CommandRegistry(registries.Registry):
    """A registry specialized for commands."""

    def register(self, cmd):
        super(CommandRegistry, self).register(cmd.name, cmd,
                                              help_string=cmd.description)


# All commands are registered here, defining what run() supports
command_registry = CommandRegistry()


class Command(object):

    name = 'Must be set by daughter classes'
    description = 'Must be set by daughter classes'

    def __init__(self, out=None, err=None, _vm=None):
        """Command constructor.

        :param out: A stream for command output.

        :param err: A stream for command errors.

        :param _vm: An existing vms.VM instance. For tests only.
        """
        self.vm = _vm
        if out is None:
            out = sys.stdout
        if err is None:
            err = sys.stderr
        self.out = out
        self.err = err
        self.parser = ArgParser(self.name, self.description)

    def parse_args(self, args):
        self.options = self.parser.parse_args(args, self.out, self.err)
        return self.options


class Help(Command):

    name = 'help'
    description = 'Describe uci-vms commands.'

    def __init__(self, **kwargs):
        super(Help, self).__init__(**kwargs)
        self.parser.add_argument(
            'commands', metavar='COMMAND', nargs='*',
            help='Display help for each command.'
            ' List all command descriptions if none is given.')

    def run(self):
        if not self.options.commands:
            self.out.write('Available commands:\n')
            for cmd_name in command_registry.keys():
                cmd_class = command_registry.get(cmd_name)
                self.out.write('\t{}: {}\n'.format(cmd_class.name,
                                                   cmd_class.description))
            return
        for cmd_name in self.options.commands:
            try:
                cmd_class = command_registry.get(cmd_name)
            except KeyError:
                cmd_class = None
            if cmd_class:
                cmd = cmd_class()
                cmd.parser.print_help(self.out)
            else:
                msg = '"{}" is not a known command\n'.format(cmd_name)
                self.err.write(msg)
        return 0


command_registry.register(Help)


class VmCommand(Command):
    """A command applying to a given vm.

    This is not a command by itself but a base class for concrete commands.
    """

    def __init__(self, **kwargs):
        super(VmCommand, self).__init__(**kwargs)
        self.parser.add_argument(
            'vm_name',
            help='Virtual machine section in the configuration file.')

    def parse_args(self, args):
        super(VmCommand, self).parse_args(args)
        self.parse_vm_arg()
        return self.options

    def parse_vm_arg(self):
        self.vm_name = self.options.vm_name
        if self.vm is None:
            conf = config.VmStack(self.vm_name)
            try:
                kls_name = conf.get('vm.class', convert=False)
            except config_errors.OptionMandatoryValueError:
                raise errors.UciVmsError('"{name}" must define vm.class.',
                                         name=self.vm_name)
            # Even if defined, the value may be wrong
            try:
                kls = conf.get('vm.class')
            except config_errors.OptionMandatoryValueError:
                raise errors.InvalidVmClass(self.vm_name, kls_name)
            self.vm = kls(conf)
        return self.options


class Config(VmCommand):

    name = 'config'
    description = 'Manage a virtual machine configuration.'

# FIXME: The full help should be the following but that doesn't fit well with
# the Help command for now -- vila 2014-03-26

# Display the active value for option NAME.
#
# If NAME is not given, --all .* is implied (all options are displayed).
#
# If --all is specified, NAME is interpreted as a regular expression and all
# matching options are displayed (without resolving option references in the
# value). The active value is the first one displayed for each option.
#
# NAME=value without spaces sets the value.
#
# --remove NAME remove the option definition.

    def __init__(self, **kwargs):
        super(Config, self).__init__(**kwargs)
        self.parser.add_argument(
            'name', nargs='?', help='''The option name.''')
        self.parser.add_argument(
            '--remove', '-r', action="store_true", help='Remove the option.'),
        self.parser.add_argument(
            '--all', '-a', action="store_true",
            help='Display all the defined values for the matching options.'),

    def parse_args(self, args):
        # Work around argparse not providing a proper way to mix positional
        # arguments and options. If an option arg is used, the 'name'
        # positional arg is not set and ends up in 'rest'.
        self.options, rest = self.parser.parse_known_args(
            args, self.out, self.err)
        self.parse_vm_arg()
        o = self.options
        if o.all or o.remove:
            # Get 'name' back from 'rest' if available
            if rest:
                o.name = rest.pop(0)
        # If we still have args left, it's an error
        if rest:
            err_orig = sys.stderr
            try:
                sys.stderr = self.err
                msg = 'unrecognized arguments: {}'
                self.parser.error(msg.format(' '.join(rest)))
            finally:
                sys.stderr = err_orig
        if o.remove:
            if o.all:
                raise errors.UciVmsError(
                    '--remove and --all are mutually exclusive.')
            if o.name is None:
                raise errors.UciVmsError(
                    '--remove expects an option to remove.')
        if o.name is not None and '=' in o.name:
            if o.all:
                raise errors.UciVmsError('Only one option can be set.')
        return o

    def list(self, name):
        # Display the value as a string
        value = self.vm.conf.get(name, expand=True, convert=False)
        if value is not None:
            # No quoting needed (for now)
            self.out.write(value)
        else:
            raise errors.ConfigOptionNotFound(name)

    def list_matching(self, re_str):
        cur_store_id = None
        cur_section_id = None
        names = re.compile(re_str)
        for (store, section, name, value) in self.vm.conf.iter_options():
            if names.search(name) is None:
                continue
            if cur_store_id != store.id:
                # Explain where the options are defined
                self.out.write('{}:\n'.format(store.id,))
                cur_store_id = store.id
                cur_section_id = None
            if (section.id is not None and cur_section_id != section.id):
                # Display the section id as it appears in the store
                # (None doesn't appear by definition)
                self.out.write('  [{}]\n'.format(section.id,))
            cur_section_id = section.id
            # No quoting needed (for now)
            self.out.write('  {} = {}\n'.format(name, value))

    def run(self):
        o = self.options
        if o.remove:
            try:
                self.vm.conf.remove(o.name)
            except config_errors.NoSuchConfigOption as e:
                raise errors.ConfigOptionNotFound(e.name)
        elif o.name is not None and '=' in o.name:
            # Set the option value
            name, value = o.name.split('=', 1)
            self.vm.conf.set(name, value)
        else:
            # List the options
            if o.name is None:
                # Defaults to all options
                o.name = '.*'
                o.all = True
            if o.all:
                self.list_matching(o.name)
            else:
                self.list(o.name)


command_registry.register(Config)


class Setup(VmCommand):

    name = 'setup'
    description = 'Setup a virtual machine.'

    def __init__(self, **kwargs):
        super(Setup, self).__init__(**kwargs)
        self.parser.add_argument(
            '--download', '-d', action="store_true",
            help='Force download of the required image.')
        self.parser.add_argument(
            '--ssh-keygen', '-k', action="store_true",
            help='Generate the ssh keys for the machine).')

    def run(self):
        if self.options.download:
            self.vm.download(force=True)
        if self.options.ssh_keygen:
            self.vm.ssh_keygen(force=True)

        state = self.vm.state()
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state in('shut off', 'STOPPED'):
            self.vm.undefine()
        elif state in ('running', 'RUNNING'):
            raise errors.VmRunning(self.vm_name)
        self.vm.install()
        return 0


command_registry.register(Setup)


class Start(VmCommand):

    name = 'start'
    description = 'Start an existing virtual machine.'

    def run(self):
        state = self.vm.state()
        if state is None:
            raise errors.VmUnknown(self.vm_name)
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state in ('running', 'RUNNING'):
            raise errors.VmRunning(self.vm_name)
        self.vm.start()
        return 0


command_registry.register(Start)


class Shell(VmCommand):

    name = 'shell'
    description = 'Run a command on an existing virtual machine.'

    def __init__(self, **kwargs):
        super(Shell, self).__init__(**kwargs)
        self.parser.add_argument(
            'command', help='The command to run on the vm.', nargs='?')
        self.parser.add_argument(
            'args', help='The arguments for the command to run on the vm.',
            nargs=argparse.REMAINDER)

    def run(self):
        state = self.vm.state()
        if state is None:
            raise errors.VmUnknown(self.vm_name)
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state not in ('running', 'RUNNING'):
            raise errors.VmNotRunning(self.vm_name)
        retcode = self.vm.shell(self.options.command, *self.options.args)
        return retcode


command_registry.register(Shell)


class Stop(VmCommand):

    name = 'stop'
    description = 'Stop an existing virtual machine.'

    def run(self):
        state = self.vm.state()
        if state is None:
            raise errors.VmUnknown(self.vm_name)
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state not in ('running', 'RUNNING'):
            raise errors.VmNotRunning(self.vm_name)
        self.vm.poweroff()
        return 0


command_registry.register(Stop)


class Teardown(VmCommand):

    name = 'teardown'
    description = 'Teardown a virtual machine.'

    def run(self):
        state = self.vm.state()
        if state is None:
            raise errors.VmUnknown(self.vm_name)
        # FIXME: states need to be defined uniquely across the various vms
        # implementations -- vila 2014-01-17
        if state in ('running', 'RUNNING'):
            raise errors.VmRunning(self.vm_name)
        self.vm.undefine()
        return 0


command_registry.register(Teardown)


def run(args=None):
    if args is None:
        args = sys.argv[1:]
    if not args:
        cmd = Help()
    else:
        cmd_name = args[0]
        args = args[1:]
        try:
            cmd_class = command_registry.get(cmd_name)
            cmd = cmd_class()
        except KeyError:
            cmd = Help()
            args = [cmd_name]
    try:
        cmd.parse_args(args)
        sys.exit(cmd.run())
    except errors.BaseError, e:
        sys.stderr.write('ERROR: {!r}\n'.format(e))
        sys.exit(-1)
