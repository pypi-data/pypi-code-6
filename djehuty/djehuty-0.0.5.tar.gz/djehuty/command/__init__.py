# -*- coding: utf-8 -*-

from cliff.command import Command as CliffCommand


class Result(object):

    def __init__(self, result):
        self.value = result


class Command(CliffCommand):

    def run(self, parsed_args):
        result = self.take_action(parsed_args)
        return Result(result) if result is not None else 0
