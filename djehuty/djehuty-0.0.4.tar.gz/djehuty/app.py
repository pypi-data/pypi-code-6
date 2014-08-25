# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

from cliff.app import App as CliffApp
from cliff.commandmanager import CommandManager
from cliff.interactive import InteractiveApp

from pyramid.decorator import reify

from djehuty import __version__
from djehuty.command import Result


class App(CliffApp):

    COMMON_ARGS_DEF = {
        'user': {
            'short': 'u',
            'info': {'help': 'user name'}
        },
        'room': {
            'short': 'r',
            'info': {'help': 'room name'}
        },
    }

    def __init__(self, args_def=None, stdin=None, stdout=None, stderr=None,
                 interactive_app_factory=InteractiveApp):
        self.__args_def = args_def or {}
        CliffApp.__init__(self, 'djehuty', __version__, CommandManager('djehuty.commands'),
                          stdin=stdin, stdout=stdout, stderr=stderr,
                          interactive_app_factory=interactive_app_factory)

    def build_option_parser(self, description, version, argparse_kwargs=None):
        parser = CliffApp.build_option_parser(self, description, version, argparse_kwargs)
        for k, v in self.args_def.iteritems():
            parser.add_argument(
                *((['-{}'.format(v['short'])] if 'short' in v else []) + ['--{}'.format(k)]),
                **v.get('info', {})
            )
        return parser

    @reify
    def args_def(self):
        d = self.__args_def.copy()
        d.update(self.COMMON_ARGS_DEF)
        return d


def main():
    result = App().run(None)
    if isinstance(result, Result):
        print(result.value)
        result = 0
    sys.exit(result)
