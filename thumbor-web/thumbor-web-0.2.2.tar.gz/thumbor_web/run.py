#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse

from thumbor_web.app import create_app


def main():
    args = parse_arguments()
    app = create_app(args.conf, debug=args.debug)
    app.run(debug=args.debug, host=args.bind, port=args.port)


def parse_arguments(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default="5000", help="Port to start the server with.")
    parser.add_argument('--bind', '-b', default="0.0.0.0", help="IP to bind the server to.")
    parser.add_argument('--conf', '-c', default='marketplace_v2/config/local.conf', help="Path to configuration file.")
    parser.add_argument('--debug', '-d', action='store_true', default=False, help='Indicates whether to run in debug mode.')

    options = parser.parse_args(args)
    return options
