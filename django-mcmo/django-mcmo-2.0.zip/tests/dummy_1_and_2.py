"""
Running command defined in app1 and app2
Everything should work and both handle_noargs functions should be called
"""

from mock import patch

from .base import TestCase

from tests.app1.management.commands.dummy import Command as Command_1
from tests.app2.management.commands.dummy import Command as Command_2


output = []


def handle_noargs(cmd_class, out):
    def f(cmd, **options):
        output.append(out)
        super(cmd_class, cmd).handle_noargs(**options)
    return f


class DummyOverrideTests(TestCase):

    apps = ('app1', 'app2')

    def test_options(self):
        self.assertInOptions('dummy', '--dummy-zero')
        self.assertInOptions('dummy', '--dummy-one')
        self.assertInOptions('dummy', '--dummy-two')
        self.assertNotInOptions('dummy', '--dummy-three')

    @patch.object(Command_2, 'handle_noargs',
                  new=handle_noargs(Command_2, 'dummy2'))
    @patch.object(Command_1, 'handle_noargs',
                  new=handle_noargs(Command_1, 'dummy1'))
    def test_called(self):
        global output
        output = []
        self.call_command('dummy', dummy_one='', dummy_two='')
        self.assertListEqual(output, ['dummy2', 'dummy1'])
