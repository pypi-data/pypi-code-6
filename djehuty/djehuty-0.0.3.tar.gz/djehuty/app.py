# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

from cStringIO import StringIO
from contextlib import closing

from cliff.app import App as CliffApp
from cliff.commandmanager import CommandManager
from cliff.interactive import InteractiveApp

from djehuty import __version__
from djehuty.command import Result


class App(CliffApp):

    def __init__(self, stdin=None, stdout=None, stderr=None,
                 interactive_app_factory=InteractiveApp):
        CliffApp.__init__(self, 'djehuty', __version__, CommandManager('djehuty.commands'),
                          stdin=stdin, stdout=stdout, stderr=stderr,
                          interactive_app_factory=interactive_app_factory)

    def build_option_parser(self, description, version, argparse_kwargs=None):
        parser = CliffApp.build_option_parser(self, description, version, argparse_kwargs)
        parser.add_argument(
            u'-u', u'--user',
            help=u'user name',
        )
        parser.add_argument(
            u'-r', u'--room',
            help=u'room name',
        )
        return parser

    @classmethod
    def run_and_get_result(self, argv):
        with closing(StringIO()) as stdout, closing(StringIO()) as stderr:
            result = App(stdout=stdout, stderr=stderr).run(argv)
            if isinstance(result, Result):
                return result.value
            elif result == 0:
                return stdout.getvalue()
            else:
                return stderr.getvalue()


def main():
    result = App().run(None)
    if isinstance(result, Result):
        print(result.value)
        result = 0
    sys.exit(result)
