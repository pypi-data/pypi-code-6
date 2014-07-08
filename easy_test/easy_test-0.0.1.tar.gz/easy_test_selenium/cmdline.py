import sys
from importlib import import_module

def get_command(cmd):
    return import_module('easy_test_selenium.commands.%s'%cmd)

def execute(argv=None, settings=None):
    # Get arguments
    if argv is None:
        argv = sys.argv
    app = argv[1]
    name = len(argv) > 2 and argv[2] or None

    if app=='test':
        if name is None:
            name = 'all'
    # Execute command
    cmd = get_command(app)
    cmd.run_command(name)

    print 'running command ...'

if __name__ == '__main__':
    execute()
