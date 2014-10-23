#!/usr/bin/env python

from __future__ import print_function
import argparse
import requests
import json
import sys


class CmdClient(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = 'http://%s:%d/cmd/' % (host, port)

    def request(self, cmd, **kwargv):
        try:
            rep = requests.post(self.url + cmd, json=kwargv)
        except requests.exceptions.ConnectionError:
            print('connect fail:(%s:%d)' % (self.host, self.port),
                  file=sys.stderr)
            raise SystemExit
        return rep.json()


def partial_args(cl_argv):
    args = {}
    if cl_argv is not None:
        for item in cl_argv:
            parts = item.split('=')
            if len(parts) != 2:
                print('invalid arg: `%s`' % item, file=sys.stderr)
                raise SystemExit
            args[parts[0]] = parts[1]
    return args


def get_args():
    parser = argparse.ArgumentParser('http-cmd client')
    parser.add_argument('-i', '--host', dest='host', default='127.0.0.1',
                        help='cmd server host')
    parser.add_argument('-p', '--port', dest='port', type=int, default=5000,
                        help='cmd server port')
    parser.add_argument('cmd', help='cmd to request')
    parser.add_argument('args', metavar='arg', nargs='*', help='args of cmd')
    return parser.parse_args()


def main():
    args = get_args()
    cli = CmdClient(args.host, args.port)
    rep = cli.request(args.cmd, **partial_args(args.args))
    print(json.dumps(rep, indent=2))


if __name__ == '__main__':
    main()
