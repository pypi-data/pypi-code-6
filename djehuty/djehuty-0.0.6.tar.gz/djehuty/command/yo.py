# -*- coding: utf-8 -*-

from djehuty.command import Command


class Yo(Command):
    '''echo yo'''

    def get_parser(self, prog_name):
        parser = Command.get_parser(self, prog_name)
        parser.add_argument('-g', '--greeting',
                            default='yo',
                            help='greeting message')
        return parser

    def take_action(self, parsed_args):
        return ('@{} '.format(self.app_args.user) if self.app_args.user else '') + parsed_args.greeting
