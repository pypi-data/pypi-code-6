"""
This file is part of snakewatch.

snakewatch is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

snakewatch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with snakewatch.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import print_function, absolute_import, unicode_literals, division

import argparse
import importlib
import logging
import os
import signal
import stat
import sys

from logging.handlers import RotatingFileHandler

from . import (
    NAME, VERSION, DESCRIPTION, USER_PATH, URL, AUTHOR, AUTHOR_EMAIL,
    LOG_FILE, LOG_LEVEL, LOG_BACKUP_COUNT, LOG_MAX_BYTES, LOG_FORMAT, LOG_TO_STDOUT
)
from .util import AbortError, get_read_object, config, ui_print


_logger = logging.getLogger()
_logger.setLevel(LOG_LEVEL)

_log_handler = logging.StreamHandler()
_log_handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
_logger.addHandler(_log_handler)

parser = None


def get_logger(name):
    """Get a logging instance consistent with the main logger"""
    if sys.version_info > (2, 7):
        return _logger.getChild(name)
    return logging.getLogger('.'.join([_logger.name, name]))


def release_action_resources():
    """Release all resources loaded by all actions"""
    if config() is None:
        return

    for action in config().actions:
        try:
            action.release_resources()
        except:
            ui_print().error(
                'Unable to release resources for action {}'.format(action.__class__.__name__),
                str(action.cfg), sep='\n'
            )


def main(initial_args=None, handle_signals=True):
    global _log_handler, parser

    if initial_args is None:
        initial_args = sys.argv[1:]

    log_to_file = True
    if not os.path.exists(USER_PATH):
        try:
            os.makedirs(USER_PATH)
        except OSError:
            log_to_file = False
            print('Unable to create snakewatch settings/log directory.',
                  'Please create the directory {}'.format(USER_PATH),
                  sep='\n', file=sys.stderr)

    if not os.access(USER_PATH, os.W_OK):
        try:
            mode = stat.S_IWRITE
            if not sys.platform == 'win':
                st = os.stat(USER_PATH)
                mode = mode | st.mode
            os.chmod(USER_PATH, mode)
        except OSError:
            log_to_file = False
            print('Unable to write to snakewatch settings/log directory.',
                  'Please set write permissions to the directory {}'.format(USER_PATH),
                  sep='\n', file=sys.stderr)

    if log_to_file and not LOG_TO_STDOUT:
        _logger.removeHandler(_log_handler)
        _log_handler.close()

        _log_handler = RotatingFileHandler(
            filename=LOG_FILE,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT,
        )

        _log_handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
        _logger.addHandler(_log_handler)
    
    parser = argparse.ArgumentParser(
        prog=NAME,
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    global_args = parser.add_argument_group('Global')
    parser.add_argument(
        '-v', '--version', 
        action='version', 
        version='\n'.join([NAME, VERSION, '', '{} <{}>'.format(AUTHOR, AUTHOR_EMAIL), URL])
    )
    parser_config = global_args.add_mutually_exclusive_group()
    parser_config.add_argument(
        '-c', '--config', 
        help='which configuration file to use'
    )
    parser_config.add_argument(
        '--no-config', action='store_true',
        help='don\'t use any configuration file (including the default), print everything'
    )
    parser.add_argument(
        '-n', '--lines',
        default=0, type=int,
        help='start LINES from end of the file, use -1 to start at the beginning',
    )

    watch_loc_group = global_args.add_mutually_exclusive_group()
    watch_loc_group.add_argument(
        '-w', '--watch', 
        help='which file to watch'
    )
    watch_loc_group.add_argument(
        '-r', '--read',
        action='store_true',
        help='read input from stdin'
    )

    # Only one mode for now, so exclude all this stuff.

    # import imp
    # import importlib
    # from snakewatch import mode as mode_package
    # suffixes = tuple([suffix[0] for suffix in imp.get_suffixes()])
    # mode_names = set([
    #     os.path.splitext(module)[0]
    #     for module in os.listdir(mode_package.__path__[0])
    #     if module.endswith(suffixes)
    # ])
    # available_modes = dict()
    # for mode_name in mode_names:
    #     if mode_name == '__init__':
    #         continue
    #     try:
    #         mode_module = importlib.import_module('snakewatch.mode.{}'.format(mode_name))
    #     except ImportError:
    #         _logger.exception('Could not load mode module {}'.format(mode_name))
    #         continue
    #     else:
    #         available_modes[mode_name] = mode_module
    #
    #     setup_arguments = getattr(mode_module, 'setup_arguments', None)
    #     if setup_arguments and callable(setup_arguments):
    #         try:
    #             setup_arguments(parser)
    #         except:
    #             _logger.exception('{} mode has arguments but setup failed'.format(mode_name))
    #
    # if not available_modes:
    #     _logger.critical('No modes are available')
    #     return 1

    # parser.add_argument(
    #     '-m', '--mode',
    #     choices=available_modes,
    #     default='Console',
    #     help='which mode to use'
    # )

    try:
        args = parser.parse_args(initial_args)
    except SystemExit:
        return

    args.mode = 'Console'

    _logger.debug('{}\n'.format('=' * 40))

    mode = importlib.import_module('.mode.Console', __package__)
    handler = getattr(mode, '{}Mode'.format(args.mode), None)
    if not handler or not callable(handler):
        _logger.critical('{} mode structure is not valid'.format(args.mode))
        sys.exit(1)

    handler = handler()

    if handle_signals:
        if not sys.platform.startswith('win'):
            signal.signal(signal.SIGHUP, handler.handle_signal)
            signal.signal(signal.SIGQUIT, handler.handle_signal)
        signal.signal(signal.SIGINT, handler.handle_signal)
        signal.signal(signal.SIGTERM, handler.handle_signal)
        signal.signal(signal.SIGABRT, handler.handle_signal)

    try:
        handler.run(get_read_object(args), args)
    except AbortError:
        pass
    except:
        if LOG_LEVEL == logging.DEBUG:
            raise
        import traceback
        exc_type, exc_value = sys.exc_info()[:2]
        exc_traceback = traceback.extract_stack()
        handler.fatal_error(exc_type, exc_value, exc_traceback)
        return 1
    finally:
        release_action_resources()

    _logger.debug('snakewatch exiting\n')
    _log_handler.close()

if __name__ == '__main__':
    sys.exit(main() or 0)
