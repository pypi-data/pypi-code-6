#!/usr/bin/env python
"""
jinjaconfig.py  --values="{'celery': 'con examples/example.conf
"""
from __future__ import with_statement
import argparse
try: import simplejson as json
except ImportError: import json
import sys, os
from jinja2 import TemplateError, Environment, FileSystemLoader, StrictUndefined, UndefinedError

def parse_arguments():

    parser = argparse.ArgumentParser(description="A jinja2 renderer receiving arguments from commandline. \
                                                  Useful for generating config files in deployment enviroments")

    parser.add_argument('--values', metavar='values', type=str, help='json encoded values', nargs='?',
                        default='{}', required=True)
    parser.add_argument('template', metavar='file', type=str, nargs='?', help='template to parse')

    args = parser.parse_args()

    env = Environment(loader=FileSystemLoader(os.getcwd()), undefined=StrictUndefined)

    try:
        values = json.loads(args.values)
    except ValueError:
        raise argparse.ArgumentTypeError('values are not JSON encoded')

    try:
        t = env.get_template(args.template)
    except IOError:
        raise argparse.ArgumentTypeError("Can't read %s " % args.template)
    except TemplateError:
        raise argparse.ArgumentTypeError("%s is not a valid Jinja2 template" % args.template)

    try:
        result = t.render(values)
    except UndefinedError as e:
        raise argparse.ArgumentTypeError('Missing element in values: ' + e.message)

    sys.stdout.write(result)

def main():
    try:
        parse_arguments()
    except argparse.ArgumentTypeError as error:
        print error.message

if __name__ == '__main__':
    main()