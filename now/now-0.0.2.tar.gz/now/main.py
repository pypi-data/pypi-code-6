import os
import sys
import argparse
from datetime import datetime
from now import config

CONFIG_PATH = "~/.nowrc"
OUTPUT_PATH = "~/.now.txt"


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('message', nargs='*')
    return parser


def get_output_file():
    nowrc = config.Nowrc.from_file(os.path.expanduser(CONFIG_PATH))
    path = nowrc['write_to'] or OUTPUT_PATH
    path = os.path.expanduser(path)
    abspath = os.path.abspath(path)
    if path != abspath:
        sys.stderr.write("Error: write_to parameter in ~/.nowrc "
                         "should be an absolute path.\n")
        return None
    output = open(path, 'a+b')
    return output


def _main(args, encoding="utf-8"):
    now = datetime.utcnow()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    parser = make_parser()
    parsed, extra = parser.parse_known_args(args)
    if not parsed.message and not extra:
        sys.stderr.write("You forgot to say what you're doing.\n")
        return 1
    message = "{0} {1}".format(" ".join(parsed.message), " ".join(extra))
    line = "{0} {1}".format(timestamp, message)
    output = get_output_file()
    if output is None:
        return 1
    with output:
        output.write(line.encode(encoding))
        output.write(b'\n')


def main():
    args = sys.argv[1:]
    result = _main(args)
    sys.exit(result)
