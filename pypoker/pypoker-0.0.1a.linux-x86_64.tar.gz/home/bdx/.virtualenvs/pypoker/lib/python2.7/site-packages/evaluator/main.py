import logging
import sys
from cliff.app import App
from cliff.commandmanager import CommandManager


class PyPoker(App):

    log = logging.getLogger(__name__)

    def __init__(self):
        super(PyPoker, self).__init__(
            description='CLI for evaluating poker hands',
            version='0.0.1a',
            command_manager=CommandManager('pypoker.app')
        )

    def initialize_app(self, argv):
        self.log.debug('initialize app')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare to run command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    app = PyPoker()
    return app.run(argv)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

