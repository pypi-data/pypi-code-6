#!/usr/bin/env python3

import argparse

from collections import namedtuple

from .configparser import JSONConfigParser
from .utils import call

parser = argparse.ArgumentParser()

# positional arguments
parser.add_argument(
    "file", 
    help="Path to config file, may be relative or absolute."
    )
parser.add_argument("command", help="Action to take on the config file")

# optional arguments
parser.add_argument(
    "-p",
    "--path", 
    help="Specific field to act on. If not passed, act on the whole file.",
    default="$"
    )

parser.add_argument(
    "-o",
    "--other",
    help="Used with the addfile command to read in another file.",
    default=""
    )

parser.add_argument(
    "-v",
    "--value",
    help="Used with several commands that require a value.",
    default=""
    )

parser.add_argument(
    "-m",
    "--multi",
    help="Boolean flag for the append command for handling multiple results along the path. Defaults to false.",
    action="store_true"
    )

parser.add_argument(
    '-c',
    '--convert',
    help="Optional conversion flag.",
    default=False
    )


def cli():
    args = parser.parse_args()
    conf = JSONConfigParser(source=args.file, storage=args.file)
    call(args.command, conf, args)
    conf.write()   

if __name__ == "__main__":
    cli()
