# -*- coding: utf-8 -*-

import sys
import logging

from cliff.app import App
from cliff.commandmanager import CommandManager

class Occult(App):
    log = logging.getLogger(__name__)

    def __init__(self):
        super(Occult, self).__init__(
            description='Xcode Project Toolkit',
            version='0.1',
            command_manager=CommandManager('occult.manager')
        )

    def initialize_app(self, argv):
        pass

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        pass

def main(argv=sys.argv[1:]):
    occult = Occult()
    return occult.run(argv)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))