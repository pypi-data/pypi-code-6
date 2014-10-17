#!/usr/bin/env python

from __future__ import print_function
import requests
import json
import sys


class CmdClient(object):

    def __init__(self, addr):
        self.addr = addr
        self.url = 'http://%s/cmd/' % addr

    def request(self, cmd, **kwargv):
        rep = requests.post(self.url + cmd, json=kwargv)
        return rep.json()


def partial_args():
    args = {}
    for item in sys.argv[3:]:
        parts = item.split('=')
        if len(parts) != 2:
            print('invalid arg: `%s`' % item, file=sys.stderr)
        args[parts[0]] = parts[1]
    return args


def main():
    if len(sys.argv) < 3:
        print('usage: httpcmd ip:port cmd k=v ...', file=sys.stderr)
        raise SystemExit
    cli = CmdClient(sys.argv[1])
    rep = cli.request(sys.argv[2], **partial_args())
    print(json.dumps(rep, indent=2))


if __name__ == '__main__':
    main()
