# =============================================================================
# Copyright [2014] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
"""
>>> # THIS IS ONLY ADDED FOR TESTING
>>> import sys
>>> sys.argv = ['test_app', 'subparsed1', 'test']
>>> # THIS IS ONLY ADDED FOR TESTING

>>> from cloudlib import arguments
>>> arguments_dict = {
...     'shared_args': {
...         'shared_option1': {
...             'commands': ['--shared-option1'],
...             'help': 'Helpful Information'
...         }
...     },
...     'optional_args': {
...         'option1': {
...             'commands': ['--option1'],
...             'help': 'Helpful Information'
...         }
...     },
...     'positional_args': {
...         'possitional1': {
...             'help': 'Helpful Information',
...             'nargs': 1
...         }
...     },
...     'subparsed_args': {
...         'subparsed1': {
...             'help': 'Helpful Information',
...             'shared_args': ['shared_option1'],
...             'optional_args': {
...                 'mutually_exclusive': {
...                     'some_value': [
...                         'option1',
...                         'option2'
...                     ]
...                 },
...                 'option1': {
...                     'commands': ['--option1'],
...                     'default': False,
...                     'action': 'store_true',
...                     'help': 'Helpful Information'
...                 },
...                 'option2': {
...                     'commands': ['--option2'],
...                     'default': False,
...                     'action': 'store_true',
...                     'help': 'Helpful Information'
...                 },
...                 'other_option1': {
...                     'commands': ['--other-option3', '-O'],
...                     'metavar': '[STRING]',
...                     'type': str,
...                     'help': 'Helpful Information'
...                 }
...             }
...         }
...     }
... }
>>> args = arguments.ArgumentParserator(arguments_dict=arguments_dict)
>>> parsed_args = args.arg_parser()
>>> type(parsed_args)
<type 'dict'>
"""

import argparse
import os

from cloudlib import parse_ini


class ArgumentParserator(object):

    def __init__(self, arguments_dict, usage='%(prog)s', env_name='CLOUDLIB',
                 epilog=None, title=None, detail=None, description=None):
        """All variables are optional, and generally cosmetic.

            * If you wanted to change the program usage example, and or
              application name set the `usage` variable.

            * `env_name` pertains to any environment variables that are set and
              will be used as a prefix within the name of the available
              environment variable.

            * `eplilog` will allow you to set a string that is rendered at the
              end of the command when using ``--help``.

            * `detail` provides a short detailed information section under the
              example usage section.

            * `description` allows for more data to be used when describing the
              application.

        :param usage: `str`
        :param env_name: `str`
        :param epilog: `str`
        :param title: `str`
        :param detail: `str`
        :param description: `str`


        Example Usage:

        The arguments dictionary has several special keys which are reserved
        for building the CLI arguments.
        """
        self.usage = usage
        self.env_name = env_name
        self.epilog = epilog
        self.title = title
        self.detail = detail
        self.description = description
        self.arguments = arguments_dict

    def _add_opt_argument(self, opt_args, arg_parser):
        """Add an argument to an instantiated parser.

        :param opt_args: ``dict``
        :param arg_parser: ``object``
        """
        if 'mutually_exclusive' in opt_args:
            exclusive_args = opt_args.pop('mutually_exclusive')
            for ex_args in exclusive_args.keys():
                ex_group = arg_parser.add_mutually_exclusive_group()
                ex_dict = {}
                for ex_arg in exclusive_args[ex_args]:
                    ex_dict[ex_arg] = opt_args.pop(ex_arg)
                else:
                    self._add_opt_argument(
                        opt_args=ex_dict, arg_parser=ex_group
                    )

        for opt_arg in opt_args.keys():
            _opt_arg = opt_args[opt_arg]
            arg_parser.add_argument(
                *_opt_arg.pop('commands'),
                **_opt_arg
            )

    def _setup_parser(self):
        """Setup a configuration parser.

        Contains built in ``--system-config`` || ``-SC`` variable which is used
        to allow a user to set arguments in a configuration file which would
        then be processed from the "default" section of the provided file,
        assuming the file exists.

        :return: ``tuple``
        """
        # Set the prefix for environment variables
        ename = self.env_name.upper()
        env_name = '%s_CONFIG' % ename

        # Accept a config file
        conf_parser = argparse.ArgumentParser(add_help=False)
        conf_parser.add_argument(
            '--system-config',
            metavar='[FILE]',
            type=str,
            default=os.environ.get(env_name, None),
            help='Path to your Configuration file. This is an optional'
                 ' argument used to specify config. available as: env[%s]'
                 % env_name
        )
        known_args, remaining_argv = conf_parser.parse_known_args()
        conf_file = known_args.system_config
        if conf_file is not None:
            file_name = os.path.basename(conf_file)
            config = parse_ini.ConfigurationSetup(name=file_name)
            path_dir = os.path.dirname(conf_file)
            config.load_config(path=path_dir)
            config_args = config.config_args(section='default')
            known_args.__dict__.update(config_args)

        parser = argparse.ArgumentParser(
            parents=[conf_parser],
            usage=self.usage,
            description=self.description,
            epilog=self.epilog)

        # Setup for the positional Arguments
        if self.detail is not None:
            self.detail = '%s\n' % self.detail

        subparser = parser.add_subparsers(
            title=self.title, metavar=self.detail
        )

        return parser, subparser, remaining_argv

    def arg_parser(self, passed_args=None):
        """Setup argument Parsing.

        If preset args are to be specified use the ``passed_args`` tuple.

        :param passed_args: ``list``
        :return: ``dict``
        """
        parser, subpar, remaining_argv = self._setup_parser()

        optional_args = self.arguments.get('optional_args')
        if optional_args:
            self._add_opt_argument(opt_args=optional_args, arg_parser=parser)

        subparsed_args = self.arguments.get('subparsed_args')
        if subparsed_args:
            for argument in subparsed_args.keys():
                _arg = subparsed_args[argument]
                if 'optional_args' in _arg:
                    optional_args = _arg.pop('optional_args')
                else:
                    optional_args = None

                if 'shared_args' in _arg:
                    shared_args = _arg.pop('shared_args')
                else:
                    shared_args = None

                action = subpar.add_parser(
                    argument,
                    **_arg
                )
                action.set_defaults(command=argument)

                if shared_args is not None:
                    load_shared_arg = self.arguments.get('shared_args')
                    for shared_arg in shared_args:
                        self._add_opt_argument(
                            opt_args={
                                shared_arg: load_shared_arg.get(shared_arg)
                            },
                            arg_parser=action
                        )

                if optional_args is not None:
                    self._add_opt_argument(
                        opt_args=optional_args, arg_parser=action
                    )

        positional_args = self.arguments.get('positional_args')
        if positional_args:
            for argument in positional_args.keys():
                _arg = positional_args[argument]

                parser.add_argument(
                    argument,
                    **_arg
                )

        if not isinstance(passed_args, list):
            passed_args = []

        for remaining_arg in remaining_argv:
            if remaining_arg not in passed_args:
                passed_args.append(remaining_arg)

        # Return the parsed arguments as a dict
        return vars(parser.parse_args(args=passed_args))
