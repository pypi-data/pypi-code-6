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

import logging
import os
import re
import six

from colorama import init as cl_init, deinit as cl_deinit, Fore, Back, Style

from .. import config
from ..util import UIPrint, AbortError, get_read_object, ui_print, set_ui_print
from ..main import get_logger, parser

_PREPEND_MSG = '\n{0} *** [{1}{2}{0}] '.format(
    Style.RESET_ALL, Style.DIM,
    'snakewatch.{:d}'.format(os.getpid()),
)

_NOTICE_CLR = Fore.GREEN + Style.DIM
_WARNING_CLR = Fore.YELLOW + Style.BRIGHT
_ERROR_CLR = Fore.RED + Style.BRIGHT

_logger = get_logger('Console')


try:
    _input = raw_input
except NameError:
    _input = input


def setup_arguments(argparser):
    pass


class ConsoleMode(object):
    """UI Handler that outputs to sys.stdout"""

    def __init__(self, *args):
        self.closed = False
        self.cfg = None
        self.received_signal = False
        self.interrupted = False
        self.input = None
        self._waiting_for_input = None
        self.current_style = Style.RESET_ALL
        self.interactive = None
        self.watch_loc = None
        self.config_loc = None

        set_ui_print(self.print_ntc, self.print_warn, self.print_err, self.get_choice)

    def run(self, start_input, args):
        """Read in the config and start watching the input"""
        cl_init()

        if not start_input and not self.watch_loc:
            self.print_err(
                'One of \'--watch\' or \'--read\' must be provided.\n'
                'Use \'--help\' for more information.'
            )
            self.close()
            return

        self.watch_loc = start_input or self.watch_loc

        ui_kwargs = {'ui_confirm': self.confirm}
        if not args.config and not self.config_loc:
            if args.no_config:
                self.cfg = config.DefaultConfig(self, use_file=False, ui_kwargs=ui_kwargs)
            else:
                self.cfg = config.DefaultConfig(self, ui_kwargs=ui_kwargs)
                msg = 'No config provided, using {}'.format(self.cfg.source)
                if self.cfg.source == 'default':
                    msg = '\n'.join([msg, 'Consider creating {}'.format(config.DefaultConfig.file_for(self))])
                self.print_ntc(msg)
        else:
            try:
                self.cfg = config.Config(args.config or self.config_loc, ui_kwargs)
            except AbortError:
                self.close()
                return
            except Exception as err:
                self.print_err('Error in config script {}\n{!s}'.format(
                    args.config, err
                ))
                self.close()
                return

        self.config_loc = self.cfg.source
        
        self.input = start_input
        self.interrupted = False
        self.input.watch(
            self.started_callback, 
            self.output_callback, 
            self.int_callback
        )

        self.close()

    def confirm(self, msg):
        self.print_warn(msg)
        response = 'n'
        prompt = 'Is this OK? [Y/N] : '
        while prompt and not self.received_signal:
            self._waiting_for_input = True
            try:
                response = _input(prompt).lower()
            except EOFError:
                return False
            finally:
                self._waiting_for_input = False

            if response:
                response = response[0]
            prompt = 'Please enter Y or N: ' if response not in ['y', 'n'] else None
        return response == 'y'

    def fatal_error(self, exc_type, exc_value, exc_traceback):
        """Called when an unhandled exception is raised from run()"""
        if not isinstance(exc_value, six.string_types):
            msg = str(exc_value)
        else:
            msg = exc_value

        from snakewatch import LOG_LEVEL

        if LOG_LEVEL == logging.DEBUG and exc_traceback:
            import traceback
            self.print_err(''.join(traceback.format_list(exc_traceback)).rstrip('\n'))

        self.print_err(': '.join([exc_type.__name__, msg]))

    def started_callback(self):
        """Called when the watcher has successfully opened the input"""
        if self.interrupted:
            self.print_ntc('Watch resuming on {}'.format(self.input.name()))
        else:
            self.print_ntc('(press Ctrl-C to stop) Watching {}'.format(self.input.name()))
        self.interrupted = False
        
    def output_callback(self, line):
        """Called when the watcher has read a line and performed an action"""
        self.interrupted = False
        self.cfg.match(line, print, **{'end': ''})

    def int_callback(self, error):
        """Called when the watcher encounters a problem"""
        if not self.interrupted:
            self.print_err('Watch interrupted: {}'.format(error))
        self.interrupted = True
        
    def handle_signal(self, signum, frame):
        """Handle an OS signal from the user"""
        self.received_signal = True

        if self._waiting_for_input:
            self.print_err('Waiting for stdin data. Press enter to quit (use Ctrl/Cmd-D to avoid this message)')
            return

        _logger.debug('Received signal: {:d}'.format(signum))
        if self.input:
            self.input.close()

        self.close()
        
    def close(self):
        """Close any necessary resources"""
        if self.closed:
            return

        self.closed = True
        if self.interactive and not self.input:
            self.interactive.cancel()
        elif self.received_signal:
            self.print_err('Received interrupt, {}'.format('stopping' if self.interactive else 'quitting'))
        
        print(Style.RESET_ALL, end='')
        cl_deinit()

        if self.interactive:
            interactive = self.interactive
            self.__init__()
            self.interactive = interactive

    def get_choice(self, message, prompt, choices, **kwargs):
        self.print_warn(*(message,), **kwargs)
        _choices = []
        choice_range = range(1, len(choices) + 1)
        for i in choice_range:
            _choices.append('{:>2d} - {}'.format(i, choices[i-1]))
        self.print_ntc(*_choices)

        choice = None
        _prompt = prompt
        _colour = _NOTICE_CLR
        while not choice:
            try:
                _choice = _input('{}{}: {}'.format(_colour, _prompt, Style.RESET_ALL))
            except EOFError:
                print()
                return None
            _choice = map(int, re.findall(r'\d+', _choice))[0]
            if _choice not in choice_range:
                _prompt = 'Invalid choice, try again'
                _colour = _ERROR_CLR
                continue
            choice = _choice
        return choices[choice-1]

    def print_msg(self, *args, **kwargs):
        """Print a formatted message"""
        self._print(*args, **kwargs)

    def print_warn(self, *args, **kwargs):
        """Print a formatted warning message"""
        self._print(_WARNING_CLR, *args, **kwargs)

    def print_ntc(self, *args, **kwargs):
        """Print a formatted notice message"""
        self._print(_NOTICE_CLR, *args, **kwargs)
    
    def print_err(self, *args, **kwargs):
        """Print a formatted error message"""
        self._print(_ERROR_CLR, *args, **kwargs)

    def _print(self, colour='', *args, **kwargs):
        try:
            sep = kwargs['sep']
        except KeyError:
            sep = '\n'
        prepend = ''.join([_PREPEND_MSG, colour])
        msg = sep.join(args)
        msg = msg.replace('\n', prepend)
        print(''.join([prepend, msg, self.current_style]))
        print()
