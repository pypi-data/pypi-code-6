from tengs_cli import actions, settings, logger
from functools import partial

import argparse, sys

def main():
    parser = parse_args(sys.argv[1:])

    current_level = "info"
    if parser.verbose:
        current_level = "debug"

    parser.func(parser, partial(logger, current_level))

def parse_args(args):
    description = 'tengs - A command line tool to interact with http://tengs.ru'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-v', '--verbose', action='store_true')

    parsers = parser.add_subparsers()

    login_parser = parsers.add_parser("login")
    login_parser.add_argument('github_name', type=str)
    login_parser.add_argument('tengs_api_key', type=str, help="see on {0}/account".format(settings.site))
    login_parser.set_defaults(func=actions.login)

    fetch_parser = parsers.add_parser("fetch")
    fetch_parser.set_defaults(func=actions.fetch)

    submit_parser = parsers.add_parser("submit", description="it only works from teng exercise directory.")
    submit_parser.set_defaults(func=actions.submit)

    return parser.parse_args(args)
