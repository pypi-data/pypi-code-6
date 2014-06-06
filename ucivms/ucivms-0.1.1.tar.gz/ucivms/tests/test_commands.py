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
from __future__ import unicode_literals

from cStringIO import StringIO
import unittest

from uciconfig import (
    options,
    registries,
)
from ucitests import (
    assertions,
    fixtures,
)
from ucivms import (
    commands,
    config,
    errors,
    vms,
)
from ucivms.tests import (
    fixtures as vms_fixtures,
)


class TestHelpOptions(unittest.TestCase):

    def setUp(self):
        super(TestHelpOptions, self).setUp()
        self.out = StringIO()
        self.err = StringIO()

    def parse_args(self, args):
        help_cmd = commands.Help(out=self.out, err=self.err)
        return help_cmd.parse_args(args)

    def test_defaults(self):
        ns = self.parse_args([])
        self.assertEqual([], ns.commands)

    def test_single_command(self):
        ns = self.parse_args(['setup'])
        self.assertEqual(['setup'], ns.commands)

    def test_several_commands(self):
        ns = self.parse_args(['help', 'setup', 'not-a-command'])
        self.assertEqual(['help', 'setup', 'not-a-command'], ns.commands)


class TestHelp(unittest.TestCase):

    def setUp(self):
        super(TestHelp, self).setUp()
        self.out = StringIO()
        self.err = StringIO()

    def assertHelp(self, expected, args=None):
        if args is None:
            args = []
        help_cmd = commands.Help(out=self.out, err=self.err)
        help_cmd.parse_args(args)
        help_cmd.run()
        assertions.assertMultiLineAlmostEqual(self, expected,
                                              self.out.getvalue())

    def test_help_alone(self):
        self.assertHelp('''\
Available commands:
\tconfig: Manage a virtual machine configuration.
\thelp: Describe uci-vms commands.
\tsetup: Setup a virtual machine.
\tshell: Run a command on an existing virtual machine.
\tstart: Start an existing virtual machine.
\tstop: Stop an existing virtual machine.
\tteardown: Teardown a virtual machine.
''')

    def test_help_help(self):
        self.assertHelp('''\
usage: uci-vms help [-h] [COMMAND [COMMAND ...]]

Describe uci-vms commands.

positional arguments:
  COMMAND     Display help for each command. List all command descriptions if
              none is given.

optional arguments:
  -h, --help  show this help message and exit
''',
                        ['help'])


class FakeVM(vms.VM):
    """A fake VM for tests that doesn't trigger dangerous or costly calls."""

    def __init__(self, conf, vm_states=None):
        super(FakeVM, self).__init__(conf)
        self.states = vm_states
        self.install_called = False
        self.start_called = False
        self.shell_called = False
        self.shell_command = None
        self.shell_cmd_args = None
        self.undefine_called = False
        self.poweroff_called = False

    def state(self):
        return self.states.get(self.conf.get('vm.name'), None)

    def install(self):
        self.install_called = True

    def start(self):
        self.start_called = True

    def shell(self, command, *cmd_args):
        self.shell_called = True
        self.shell_command = command
        self.shell_cmd_args = cmd_args

    def poweroff(self):
        self.poweroff_called = True

    def undefine(self):
        self.undefine_called = True


def setup_fake_vm(test):
    vms_fixtures.isolate_from_disk(test)
    test.conf = config.VmStack('foo')
    test.conf.store._load_from_string('''
[foo]
vm.name=foo
vm.class=fake
vm.release=saucy
vm.cpu_model=amd64
''')
    test.addCleanup(test.conf.store.save_changes)
    # Register our fake vm class inside the registry option as that's where it
    # matters.
    vm_reg = options.option_registry.get('vm.class')
    fixtures.patch(test, vm_reg, 'registry', registries.Registry())
    vm_reg.registry.register('fake', FakeVM, 'Fake vm')
    # Install a way to decide if a given vm is running or not
    test.states = {}


class TestVmCommandOptions(unittest.TestCase):

    def setUp(self):
        super(TestVmCommandOptions, self).setUp()
        setup_fake_vm(self)
        self.out = StringIO()
        self.err = StringIO()

    def parse_args(self, args):
        vm_cmd = commands.VmCommand(out=self.out, err=self.err)
        return vm_cmd.parse_args(args)

    def test_nothing(self):
        with self.assertRaises(SystemExit):
            self.parse_args([])

    def test_defaults(self):
        ns = self.parse_args(['foo'])
        self.assertEquals('foo', ns.vm_name)


class TestVmCommand(unittest.TestCase):

    def setUp(self):
        super(TestVmCommand, self).setUp()
        setup_fake_vm(self)

    def run_cmd(self, args):
        vm_cmd = commands.VmCommand()
        vm_cmd.parse_args(args)
        vm_cmd.run()

    def test_unknown(self):
        self.conf.set('vm.name', 'I-dont-exist')
        with self.assertRaises(errors.UciVmsError):
            self.run_cmd(['I-dont-exist'])

    def test_unknown_vm_class(self):
        self.conf.set('vm.class', 'I-dont-exist')
        with self.assertRaises(errors.InvalidVmClass):
            self.run_cmd(['foo'])


class TestConfigOptions(unittest.TestCase):

    def setUp(self):
        super(TestConfigOptions, self).setUp()
        setup_fake_vm(self)
        self.out = StringIO()
        self.err = StringIO()

    def parse_args(self, args):
        conf_cmd = commands.Config(out=self.out, err=self.err)
        return conf_cmd.parse_args(args)

    def test_nothing(self):
        with self.assertRaises(SystemExit):
            self.parse_args([])

    def test_defaults(self):
        ns = self.parse_args(['foo'])
        self.assertEquals('foo', ns.vm_name)
        self.assertIs(None, ns.name)
        self.assertFalse(ns.all)
        self.assertFalse(ns.remove)

    def test_name(self):
        ns = self.parse_args(['foo', 'bar'])
        self.assertEqual('bar', ns.name)

    def assertError(self, expected):
        assertions.assertMultiLineAlmostEqual(self, expected,
                                              self.err.getvalue())

    def test_too_much_args(self):
        with self.assertRaises(SystemExit) as cm:
            self.parse_args(['foo', 'bar', 'baz'])
        self.assertEqual(2, cm.exception.message)
        self.assertError('''\
usage: uci-vms config [-h] [--remove] [--all] vm_name [name]
uci-vms config: error: unrecognized arguments: baz
''')

    def test_remove_requires_name(self):
        with self.assertRaises(errors.UciVmsError) as cm:
            self.parse_args(['foo', '--remove'])
        self.assertEqual('--remove expects an option to remove.',
                         unicode(cm.exception))

    def test_remove_all_fails(self):
        with self.assertRaises(errors.UciVmsError) as cm:
            self.parse_args(['foo', '--remove', '--all'])
        self.assertEqual('--remove and --all are mutually exclusive.',
                         unicode(cm.exception))

    def test_set_only_one_option(self):
        with self.assertRaises(errors.UciVmsError) as cm:
            self.parse_args(['foo', 'bar=baz', '--all'])
        self.assertEqual('Only one option can be set.',
                         unicode(cm.exception))


class TestConfig(unittest.TestCase):

    def setUp(self):
        super(TestConfig, self).setUp()
        setup_fake_vm(self)
        self.out = StringIO()
        self.err = StringIO()

    def run_config(self, args):
        self.vm = FakeVM(self.conf, self.states)
        cmd_config = commands.Config(_vm=self.vm, out=self.out, err=self.err)
        cmd_config.parse_args(args)
        cmd_config.run()

    def test_set_new_option(self):
        self.assertEqual(None, self.conf.get('foo'))
        self.run_config(['foo', 'foo=bar'])
        self.assertEqual('bar', self.conf.get('foo'))

    def test_set_existing_option(self):
        self.conf.set('foo', 'bar')
        self.assertEqual('bar', self.conf.get('foo'))
        self.run_config(['foo', 'foo=qux'])
        self.assertEqual('qux', self.conf.get('foo'))

    def test_remove_unknown_option(self):
        with self.assertRaises(errors.ConfigOptionNotFound):
            self.run_config(['foo', '-r', 'foo'])

    def test_remove_existing_option(self):
        self.conf.set('bar', 'baz')
        self.run_config(['foo', '-r', 'bar'])
        self.assertEqual(None, self.conf.get('bar'))

    def assertOutput(self, expected):
        assertions.assertMultiLineAlmostEqual(self, expected,
                                              self.out.getvalue())

    def test_list_option(self):
        self.conf.set('foo', 'bar')
        self.run_config(['foo', 'foo'])
        self.assertOutput('bar')

    def test_unknown_option(self):
        with self.assertRaises(errors.ConfigOptionNotFound):
            self.run_config(['foo', 'foo'])
        self.assertOutput('')

    def test_list_that_conf(self):
        self.run_config(['foo'])
        self.assertOutput('''\
.../home/uci-vms.conf:
  [foo]
  vm.name = foo
  vm.class = fake
  vm.release = saucy
  vm.cpu_model = amd64
''')

    def test_more_options(self):
        self.conf.set('one', '1')
        self.conf.set('two', '2')
        self.run_config(['foo'])
        self.assertOutput('''\
.../home/uci-vms.conf:
  [foo]
  vm.name = foo
  vm.class = fake
  vm.release = saucy
  vm.cpu_model = amd64
  one = 1
  two = 2
''')

    def test_options_several_sections(self):
        self.conf.store.unload()
        self.conf.store._load_from_string('''\
one = 1
two = 2
[foo]
one = 1
two = foo
[bar]
one = bar
two = foo
''')
        self.run_config(['foo'])
        self.assertOutput('''\
.../home/uci-vms.conf:
  one = 1
  two = 2
  [foo]
  one = 1
  two = foo
''')


class TestSetupOptions(unittest.TestCase):

    def setUp(self):
        super(TestSetupOptions, self).setUp()
        setup_fake_vm(self)
        self.out = StringIO()
        self.err = StringIO()

    def parse_args(self, args):
        self.vm = FakeVM(self.conf, self.states)
        setup = commands.Setup(_vm=self.vm, out=self.out, err=self.err)
        return setup.parse_args(args)

    def test_nothing(self):
        with self.assertRaises(SystemExit):
            self.parse_args([])

    def test_defaults(self):
        ns = self.parse_args(['foo'])
        self.assertEquals('foo', ns.vm_name)
        self.assertFalse(ns.download)
        self.assertFalse(ns.ssh_keygen)

    def test_download(self):
        ns = self.parse_args(['foo', '--download'])
        self.assertEquals('foo', ns.vm_name)
        self.assertTrue(ns.download)
        self.assertFalse(ns.ssh_keygen)

    def test_ssh_keygen(self):
        ns = self.parse_args(['foo', '--ssh-keygen'])
        self.assertEquals('foo', ns.vm_name)
        self.assertFalse(ns.download)
        self.assertTrue(ns.ssh_keygen)


class TestSetup(unittest.TestCase):

    def setUp(self):
        super(TestSetup, self).setUp()
        setup_fake_vm(self)

    def run_setup(self, args):
        self.vm = FakeVM(self.conf, self.states)
        setup = commands.Setup(_vm=self.vm)
        setup.parse_args(args)
        setup.run()

    def test_not_running(self):
        self.conf.set('vm.name', 'foo')
        self.states = {'foo': 'shut off'}
        self.run_setup(['foo'])
        self.assertTrue(self.vm.install_called)
        self.assertTrue(self.vm.undefine_called)

    def test_while_running(self):
        self.conf.set('vm.name', 'foo')
        self.states = {'foo': 'running'}
        with self.assertRaises(errors.VmRunning):
            self.run_setup(['foo'])
        self.assertFalse(self.vm.install_called)
        self.assertFalse(self.vm.undefine_called)


class TestStart(unittest.TestCase):

    def setUp(self):
        super(TestStart, self).setUp()
        setup_fake_vm(self)

    def run_start(self, args):
        self.vm = FakeVM(self.conf, self.states)
        start = commands.Start(_vm=self.vm)
        start.parse_args(args)
        start.run()

    def test_not_running(self):
        self.states = {'foo': 'shut off'}
        self.run_start(['foo'])
        self.assertTrue(self.vm.start_called)

    def test_while_running(self):
        self.states = {'foo': 'running'}
        with self.assertRaises(errors.VmRunning):
            self.run_start(['foo'])
        self.assertFalse(self.vm.start_called)

    def test_unknown(self):
        self.conf.set('vm.name', 'I-dont-exist')
        with self.assertRaises(errors.VmUnknown):
            self.run_start(['I-dont-exist'])
        self.assertFalse(self.vm.start_called)


class TestShellOptions(unittest.TestCase):

    def setUp(self):
        super(TestShellOptions, self).setUp()
        setup_fake_vm(self)
        self.out = StringIO()
        self.err = StringIO()

    def parse_args(self, args):
        self.vm = FakeVM(self.conf, self.states)
        setup = commands.Shell(_vm=self.vm, out=self.out, err=self.err)
        return setup.parse_args(args)

    def test_defaults(self):
        ns = self.parse_args(['foo'])
        self.assertEquals('foo', ns.vm_name)
        self.assertIsNone(ns.command)
        self.assertEqual([], ns.args)

    def test_command_without_arguments(self):
        ns = self.parse_args(['foo', 'doit'])
        self.assertEquals('foo', ns.vm_name)
        self.assertEqual('doit', ns.command)
        self.assertEqual([], ns.args)

    def test_command_with_arguments(self):
        ns = self.parse_args(['foo', 'doit', '-a', 'b', 'c'])
        self.assertEquals('foo', ns.vm_name)
        self.assertEqual('doit', ns.command)
        self.assertEqual(['-a', 'b', 'c'], ns.args)


class TestShell(unittest.TestCase):

    def setUp(self):
        super(TestShell, self).setUp()
        setup_fake_vm(self)

    def run_shell(self, args):
        self.vm = FakeVM(self.conf, self.states)
        shell = commands.Shell(_vm=self.vm)
        shell.parse_args(args)
        shell.run()

    def test_not_running(self):
        self.states = {'foo': 'shut off'}
        with self.assertRaises(errors.VmNotRunning):
            self.run_shell(['foo'])
        self.assertFalse(self.vm.shell_called)
        self.assertIsNone(self.vm.shell_command)
        self.assertIsNone(self.vm.shell_cmd_args)

    def test_while_running_no_command(self):
        self.states = {'foo': 'running'}
        self.run_shell(['foo'])
        self.assertTrue(self.vm.shell_called)
        self.assertIsNone(self.vm.shell_command)
        self.assertEqual((), self.vm.shell_cmd_args)

    def test_while_running_with_command(self):
        self.states = {'foo': 'running'}
        self.run_shell(['foo', 'doit', 'a', 'b', 'c'])
        self.assertTrue(self.vm.shell_called)
        self.assertEqual('doit', self.vm.shell_command)
        self.assertEqual(('a', 'b', 'c'), self.vm.shell_cmd_args)

    def test_unknown(self):
        self.conf.set('vm.name', 'I-dont-exist')
        with self.assertRaises(errors.VmUnknown):
            self.run_shell(['I-dont-exist'])
        self.assertFalse(self.vm.shell_called)


class TestStop(unittest.TestCase):

    def setUp(self):
        super(TestStop, self).setUp()
        setup_fake_vm(self)

    def run_stop(self):
        self.vm = FakeVM(self.conf, self.states)
        stop = commands.Stop(_vm=self.vm)
        stop.parse_args(['foo'])
        stop.run()

    def test_not_running(self):
        self.conf.set('vm.name', 'foo')
        self.states = {'foo': 'shut off'}
        with self.assertRaises(errors.VmNotRunning):
            self.run_stop()
        self.assertFalse(self.vm.poweroff_called)

    def test_while_running(self):
        self.conf.set('vm.name', 'foo')
        self.states = {'foo': 'running'}
        self.run_stop()
        self.assertTrue(self.vm.poweroff_called)

    def test_unknown(self):
        self.conf.set('vm.name', 'I-dont-exist')
        self.states = {}
        with self.assertRaises(errors.VmUnknown):
            self.run_stop()
        self.assertFalse(self.vm.poweroff_called)


class TestTeardown(unittest.TestCase):

    def setUp(self):
        super(TestTeardown, self).setUp()
        setup_fake_vm(self)

    def run_teardown(self, args):
        self.vm = FakeVM(self.conf, self.states)
        teardown = commands.Teardown(_vm=self.vm)
        teardown.parse_args(args)
        teardown.run()

    def test_not_running(self):
        self.conf.set('vm.name', 'foo')
        self.states = {'foo': 'shut off'}
        self.run_teardown(['foo'])
        self.assertTrue(self.vm.undefine_called)

    def test_while_running(self):
        self.conf.set('vm.name', 'foo')
        self.states = {'foo': 'running'}
        with self.assertRaises(errors.VmRunning):
            self.run_teardown(['foo'])
        self.assertFalse(self.vm.undefine_called)

    def test_unknown(self):
        self.conf.set('vm.name', 'I-dont-exist')
        self.states = {}
        with self.assertRaises(errors.VmUnknown):
            self.run_teardown(['I-dont-exist'])
        self.assertFalse(self.vm.undefine_called)


# Sketch new commands:

# shell name [-- command args*]
