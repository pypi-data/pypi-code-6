# from functools import partial
# import actions, settings, utils
#
# import argparse
#
# def main():
#     description = 'hexlet - A command line tool to interact with {0}'.format(settings.site)
#     parser = argparse.ArgumentParser(description=description)
#     parser.add_argument('-v', '--verbose', action='store_true')
#
#     parsers = parser.add_subparsers()
#
#     login_parser = parsers.add_parser("login")
#     login_parser.add_argument('github_name', type=str)
#     login_parser.add_argument('hexlet_api_key', type=str, help="see on {0}/account".format(settings.site))
#     login_parser.set_defaults(func=actions.login)
#
#     fetch_parser = parsers.add_parser("fetch")
#     fetch_parser.set_defaults(func=actions.fetch_exercise)
#
#     submit_parser = parsers.add_parser("submit", description="it only works from teng exercise directory.")
#     submit_parser.set_defaults(func=actions.submit_exercise)
#
#     args = parser.parse_args()
#
#     current_level = "info"
#     if args.verbose:
#         current_level = "debug"
#
#     args.func(args, partial(utils.logger, current_level))
