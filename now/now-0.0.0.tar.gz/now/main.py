import os
import sys
import argparse
from datetime import datetime


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('message', nargs='*')
    return parser


def get_output_file():
    path = os.path.expanduser("~/doings.txt")
    output = open(path, 'a+b')
    return output


def _main(args, encoding="utf-8"):
    now = datetime.utcnow()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    parser = make_parser()
    parsed, extra = parser.parse_known_args(args)
    if not parsed.message and not extra:
        sys.stderr.write("You forgot to say what you're doing.\n"
                         .encode(encoding))
        return 1
    message = "{0} {1}".format(" ".join(parsed.message), " ".join(extra))
    line = "{0} {1}".format(timestamp, message)
    output = get_output_file()
    with output:
        output.write(line.encode(encoding))
        output.write(b'\n')


def main():
    args = sys.argv[1:]
    result = _main(args)
    sys.exit(result)
