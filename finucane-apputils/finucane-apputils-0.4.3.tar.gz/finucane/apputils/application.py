# -*- coding: utf-8 -*-
"""finucane.apputils.application

Provides the ``Application`` class. That is all this module is expected to do.

:copyright: (c) 2014 by Sean Anthony Finucane.
:license: MIT, see LICENSE for more details.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
# Python 2.6 and newer support
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from finucane.apputils.compatibility import upgrade_namespace
upgrade_namespace(globals())

import sys
import logging
import logging.handlers
import traceback
import inspect
from uuid import uuid4 as uuid

if __python_version__['major'] > 2:
    from io import StringIO
else:
    from StringIO import StringIO as StringIO2x
    class StringIO(StringIO2x):
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()

from .namespace import Namespace, ImmutableNamespace
from .errors import ApputilsParseError
from .args import ArgumentParser
from .args import NetloggerAddressParse
from .log import LogAboveErrorFilter
from .log import JsonFormatter
from .config import ApplicationConfig


class ApplicationBase(object):
    """Most generic, public abstract base.

    If you are an application developer, this is the most general application
    class, from which all other application classes inherit. When inheriting
    from this class, a developer must implement the ``_main`` method.

    Attributes:
        app_id: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    def __init__(self, name='', version='0.1.0', description='', epilogue='',
                 stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr,
                 stdlog=sys.stderr,
                 credits=None, organization=''):
        object.__init__(self)
        self.name = name

        self.app_debug_id = None
        self._stdlog_handler = None
        self._stderr_handler = None
        self._netlog_handler = None

        self._stdlog_formatter = JsonFormatter()
        self._stderr_formatter = JsonFormatter()

        self._version = version
        self._full_name = '{n}, version {v}'.format(n=name, v=version)
        self._description = description
        self._epilogue = epilogue
        self._organization = organization
        self._credits = credits

        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.stdlog = stdlog

        self.args = None
        self.config = None
        self.log = None

        self.arg_parser = ArgumentParser(prog_name=name,
                                         prog_description=description,
                                         prog_epilogue=epilogue,
                                         prog_version=version)

        self.state = Namespace()

        # instance UUID:
        self._uuid = uuid()

    @property
    def version(self):
        return self._version

    @property
    def full_name(self):
        return self._full_name

    @property
    def description(self):
        return self._description

    @property
    def epilogue(self):
        return self._epilogue

    @property
    def organization(self):
        return self._organization

    @property
    def credits(self):
        return self._credits

    @property
    def uuid(self):
        return self._uuid

    @property
    def app_id(self):
        """A unique identifier string for the APPLICATION (not the instance)."""
        organization = str(self.organization).lower().strip().replace('.', '-').replace(' ', '_')
        name = str(self.name).lower().strip().replace('.', '-').replace(' ', '_')
        version = str(self.version).lower().strip().replace('.', '-').replace(' ', '_')
        return '{org}.{name}.{vers}'.format(org=organization, name=name, vers=version)

    @property
    def id_(self):
        """A unique identifier string for the application instance."""
        return "".join([self.app_id, '.', str(self.uuid)])

    def print(self, *args, **kwargs):
        """Print ``*args`` to ``self.stdout``, unless other out file given.

        Essentially, this is an alias for the built-in print function which
        prints to the calling instance's ``stdout`` by default.
        """
        if 'file' in kwargs:
            return print(*args, **kwargs)
        else:
            return print(*args, file=self.stdout, **kwargs)

    def _initialization(self):
        pass

    def _main(self, *args, **kwargs):
        raise NotImplementedError

    def _on_success(self):
        pass

    def _on_failure(self):
        pass

    def _finalization(self):
        pass

    def __call__(self, *args, **kwargs):
        """Alias for ``run`` method."""
        return self.run(*args, **kwargs)

    def exec_(self, *args, **kwargs):
        """Alias for ``run`` method."""
        return self.run(*args, **kwargs)

    def run(self, argv=[], *args, **kwargs):
        raise NotImplementedError('Cannot execute purely abstract method!')

    def __getstate__(self):
        state_data = {k:v for (k,v) in self.state.__dict__.items()
                      if not str(k).startswith('__')}
        state_data['__name__'] = self.name
        state_data['__organization__'] = self.organization
        state_data['__version__'] = self.version
        state_data['__description__'] = self.description
        state_data['__epilogue__'] = self.epilogue
        state_data['__credits__'] = self.credits

        return state_data

    def __setstate__(self, state):
        self.__init__()
        self._name = state.pop('__name__')
        self._organization = state.pop('__organization__')
        self._version = state.pop('__version__')
        self._description = state.pop('__description__')
        self._epilogue = state.pop('__epilogue__')
        self._credits = state.pop('__credits__')
        self.state = Namespace(data=state)


class Application(ApplicationBase):
    """Public abstract base class for applications with default features.

    If you are an application developer, this is the most general application
    class, from which all other application classes inherit. When inheriting
    from this class, a developer must implement the ``_main`` method.

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """
    def __init__(self, name='', version='0.1.0', description='', epilogue='',
                 stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr,
                 stdlog=sys.stderr,
                 credits=None, organization='', default_config_file=None):

        super().__init__(name=name, version=version, description=description,
                         epilogue=epilogue,
                         stdin=stdin, stderr=stderr, stdlog=stdlog,
                         credits=credits, organization=organization)

        self.arg_parser.add_counted_option(
            'verbose', unix_flag='v', dest='verbosity', default=0,
            help_='output additional information to stderr (more v\'s mean more output, 4 is maximal)')

        # Only enable the config option is the default config is not set to None.
        if default_config_file is not None:
            self.arg_parser.add_option(
                'config',
                type_=ApplicationConfig,
                default=ApplicationConfig(default_config_file),
                help_='path to the configuration file.')

        self.arg_parser.add_option(
            'netlogger', dest='netlogger_url',
            default=None, type_=NetloggerAddressParse,
            help_='URL(s) of the socket server(s) to which log events will be sent (e.g., "localhost:9020")')

    def run(self, argv=[], *args, **kwargs):

        self.app_debug_id = '{c}.{f}'.format(c=str(self.__class__).strip().split("'")[1],
                                             f=inspect.currentframe().f_code.co_name)

        try:
            # logging facility
            self.log = logging.getLogger(self.app_id)

            assert self.log is not None
            assert hasattr(self.log, 'critical')
            assert hasattr(self.log, 'error')
            assert hasattr(self.log, 'warning')
            assert hasattr(self.log, 'info')
            assert hasattr(self.log, 'debug')

            if self.stdlog is not None:
                # events with a level above that of ERROR
                self._stdlog_handler = logging.StreamHandler(self.stdlog)
                self._stdlog_handler.setFormatter(self._stdlog_formatter)
                self._stdlog_handler.addFilter(LogAboveErrorFilter())
                self.log.addHandler(self._stdlog_handler)

            if self.stderr is not None:
                # events with a level of ERROR and below
                self._stderr_handler = logging.StreamHandler(self.stderr)
                self._stderr_handler.setFormatter(self._stderr_formatter)
                self._stderr_handler.setLevel(logging.ERROR)
                self.log.addHandler(self._stderr_handler)

            # default logging level before full init is CRITICAL
            self.log.setLevel(logging.CRITICAL)

            # initialize the application based on given arguments.
            parsed_args = {}
            try:
                parsed_args = self.arg_parser.parse_args(argv)
            except ApputilsParseError as e:
                self.log.critical(e)
                raise e

            # grab things that should NOT be left in the args container
            if hasattr(parsed_args, 'config'):
                self.config = parsed_args.config[-1]  # all args are lists!
                vars(parsed_args)['config'] = None

            else:
                self.config = ApplicationConfig(file_path=None)

            # all arguments in ``self.args`` must be a list! Make it so.
            for key, value in vars(parsed_args).items():
                if not isinstance(value, list):
                    setattr(parsed_args, key, [value])

            self.args = ImmutableNamespace(default_factory=lambda: [None],
                                           data=vars(parsed_args))

            # logging configuration details
            assert hasattr(self.args, 'verbosity')

            logging_level = logging.CRITICAL
            if self.args.verbosity[-1] == 1:
                logging_level = logging.ERROR
            elif self.args.verbosity[-1] == 2:
                logging_level = logging.WARNING
            elif self.args.verbosity[-1] == 3:
                logging_level = logging.INFO
            elif self.args.verbosity[-1] > 3:
                logging_level = logging.DEBUG

            self.log.setLevel(logging_level)

            self._netlog_handler = []
            addresses = []
            for url in self.args.netlogger_url:
                if url is not None:
                    addresses.append({'host': url.hostname, 'port': url.port})

            for address in addresses:
                if address['host'] is not None and address['port'] is not None:
                    # a network capable logging facility (remote possibilities, etc.)
                    self._netlog_handler.append(logging.handlers.SocketHandler(address['host'], address['port']))
                    self.log.addHandler(self._netlog_handler[-1])

            self.log.debug('Preparing {app_id} environment.'.format(app_id=self.app_debug_id))

            # ready to roll!
            self.log.debug('Entering {app_id}'.format(app_id=self.app_debug_id))
            try:
                assert self.config is not None
                assert self.args is not None

                self.log.debug('config = {0!s}'.format(self.config.as_dict()))
                self.log.debug('args = {0!s}'.format(vars(self.args)))
                self.log.debug('log_name = "{0!s}"'.format(self.log.name))

                self.log.debug('Executing initialization hook.')
                self._initialization()
                self.log.debug('Executing primary function.')

                #####
                self._main(*args, **kwargs)
                #####

                self.log.debug('Primary function exited cleanly. Executing success hook.')

            except Exception as e:
                self.log.critical('An exception occurred! Executing failure hook.')
                self._on_failure()
                with StringIO() as err_msg:
                    print(e, file=err_msg)
                    traceback.print_exc(file=err_msg)
                    self.log.critical(err_msg.getvalue())
            else:
                self.log.debug('Executing success hook.')
                self._on_success()
            finally:
                self.log.debug('Executing finalization hook.')
                self._finalization()
                self.log.debug('Exiting {app_id}'.format(app_id=self.app_debug_id))

        except ApputilsParseError as e:
            pass

        finally:
            # tear-down the logging facility
            if hasattr(self, '_stdlog_handler') and self._stdlog_handler is not None:
                self.log.removeHandler(self._stdlog_handler)

            if hasattr(self, '_stderr_handler') and self._stderr_handler is not None:
                self.log.removeHandler(self._stderr_handler)

            if hasattr(self, '_netlog_handler') and self._netlog_handler is not None:
                if isinstance(self._netlog_handler, list):
                    for handler in self._netlog_handler:
                        self.log.removeHandler(handler)
                else:
                    self.log.removeHandler(self._netlog_handler)
                self._netlog_handler = None
