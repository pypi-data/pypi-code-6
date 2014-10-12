# -*- coding: utf-8 -*-

from cliff.command import Command

class Error(Command):
    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')