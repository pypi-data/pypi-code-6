from suddendeath import suddendeathmessage

from djehuty.command import Command


class Suddendeath(Command):
    '''generator suddendeath message'''

    def get_parser(self, prog_name):
        parser = Command.get_parser(self, prog_name)
        parser.add_argument('msg', help='message')
        return parser

    def take_action(self, parsed_args):
        return suddendeathmessage(parsed_args.msg.decode('utf-8'))
