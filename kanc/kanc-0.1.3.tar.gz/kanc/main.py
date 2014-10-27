#!/usr/bin/env python
from tabulate import tabulate
import os
import sys
import getopt
import getpass
import kanpyj
import json
import subprocess
import tempfile
from .command import factory
from .command.base import CommandError

class KancResourceFile:
    def __init__(self, filename):
        self.filename = filename
        self.rc_dict = {}

    def exists(self):
        return os.path.exists(self.filename)

    def read(self):
        if os.path.exists(self.filename):
            with open(self.filename) as f:
                rc = f.read()
            self.rc_dict = json.loads(rc)
        else:
            print '.kanrc file not found.'
            print 'Please type "kanc init" to create .kanrc file first'
            sys.exit(1)

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(json.dumps(self.rc_dict, indent=2))

    def get(self, key):
        return self.rc_dict[key]
    
    def set(self, key, val):
        self.rc_dict[key] = val

def usage():
    cmds = factory.create_all(None, None)
    for cmd in cmds:
        cmd.help()
    sys.exit(2)

def edit(data):
    editor = os.environ.get('EDITOR')
    if editor is None or editor == '':
        sys.stdout.write('Error: No editor is specified EDITOR')
    tmp_file = tempfile.mkstemp()
    f = file(tmp_file[1], 'w')
    f.write(data)
    f.close()
    subprocess.call([editor, tmp_file[1]])
    f = file(tmp_file[1])
    updated_data = f.read()
    f.close()
    os.remove(tmp_file[1])

    if data == updated_data:
        sys.stderr.write('Abort: The data is not updated')
        return None
    return updated_data

def main():
    args = sys.argv[1:]
    host = None
    apikey = None

    rcfile = KancResourceFile(os.path.expanduser('~/.kancrc'))
    
    # Show help if no command specified
    if len(args) == 0:
        usage()

    # Get command and subcommand
    cmd_name = args[0]
    subcmd_name = None
    cmd_args = []
    if len(args) > 1:
        subcmd_name = args[1]
    if len(args) > 2:
        cmd_args = args[2:]

    if cmd_name == 'init':
        if rcfile.exists():
            while True:
                ans = raw_input('.kanrc file already exists. Overwrite? [y/n]')
                if ans == 'y':
                    break
                elif ans == 'n':
                    print 'Abort creating .kanrc file'
                    sys.exit(1)
        sys.stdout.write('input your host: ')
        host = sys.stdin.readline().rstrip()
        apikey = getpass.getpass('input your api key: ')
        rcfile.set('host', host)
        rcfile.set('apikey', apikey)
        rcfile.set('patched', True)
        rcfile.set('currentProject', 1)
        rcfile.save()
        sys.exit(0)

    if rcfile.exists():
        rcfile.read()
        host = rcfile.get('host')
        apikey = rcfile.get('apikey')
    else:
        print '.kanrc file not found.'
        print 'Please type "kanc init" to create .kanrc file first'
        sys.exit(1)

    if rcfile.get('patched'):
        c = kanpyj.PatchedClient(host, apikey)
    else:
        c = kanpyj.Client(host, apikey)

    if cmd_name == 'help':
        usage()

    cmd = factory.create(cmd_name, c, rcfile)
    if cmd is None:
        usage()
    try:
        cmd.action(subcmd_name, cmd_args)
    except CommandError:
        cmd.help()

if __name__ == '__main__':
    main()

