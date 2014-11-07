import logging
from cliff.command import Command
from hand import Hand


class Evaluate(Command):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Evaluate, self).get_parser(prog_name)
        parser.add_argument(
            '-e',
            '--eval',
            metavar='eval',
            help="evaluate hand",
            nargs='+',
        )
        return parser

    def take_action(self, parsed_args):
        """Override take_action to parse input args and evaluate hand"""

        h = Hand(parsed_args.eval)
        for i in h.cards:
            print(i)
        print(h.get_rank())
