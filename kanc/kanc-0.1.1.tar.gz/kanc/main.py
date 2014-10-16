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

def usage():
    cmds = factory.create_all(None)
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
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hjp')
    except getopt.GetoptError as err:
        usage()

    json_mode = ('-j', '') in opts
    host = None
    apikey = None

    rcfile = os.path.expanduser('~/.kancrc')
    
    # Show help if no command specified
    if len(args) == 0:
        usage()

    if args[0] == 'init':
        if os.path.exists(rcfile):
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
        with open(rcfile, 'w') as f:
            rc_dict = {'host': host, 'apikey': apikey, 'patched': True}
            f.write(json.dumps(rc_dict, indent=2))
        sys.exit(0)

    if os.path.exists(rcfile):
        with open(rcfile) as f:
            rc = f.read()
        rc_dict = json.loads(rc)
        host = rc_dict['host']
        apikey = rc_dict['apikey']
        patched = rc_dict['patched']
    else:
        print '.kanrc file not found.'
        print 'Please type "kanc init" to create .kanrc file first'
        sys.exit(1)

    if patched:
        c = kanpyj.PatchedClient(host, apikey)
    else:
        c = kanpyj.Client(host, apikey)

    if args[0] == 'help':
        usage()
    else:
        cmd = factory.create(args[0], c)
        if cmd is None:
            usage()
        try:
            cmd.action(args[1:])
        except CommandError:
            cmd.help()

if __name__ == '__main__':
    main()

