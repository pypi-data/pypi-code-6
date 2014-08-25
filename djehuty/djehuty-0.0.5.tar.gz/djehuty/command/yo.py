# -*- coding: utf-8 -*-

from djehuty.command import Command


class Yo(Command):
    '''echo yo'''

    def take_action(self, parsed_args):
        return ('@{} '.format(self.app_args.user) if self.app_args.user else '') + 'yo'
