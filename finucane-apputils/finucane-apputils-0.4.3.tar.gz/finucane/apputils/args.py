# -*- coding: utf-8 -*-
"""finucane.apputils.args

Provides customized application argument(s) facilities and utilities. If a
customized or enhanced application argument(s) ability is needed, this is
where it should exist.

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

import argparse  # included in Python >2.7, but not 2.6

if __python_version__['major'] > 2:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse

from .errors import ApputilsParseError


def NetloggerAddressParse(url, *args, **kwargs):
    """Fetches rows from a Bigtable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by big_table.  Silly things may happen if
    other_silly_variable is not None.

    Args:
        url: An open Bigtable Table instance.

    Returns:


    Raises:
        ApputilsParseError
    """
    s_url = str(url)
    first_pass = urlparse(s_url)
    # first pass:
    if first_pass.hostname and first_pass.port:
        return first_pass
    # second pass:
    if not s_url.startswith('//'):
        s_url = "".join(["//", s_url])
    second_pass = urlparse(s_url, *args, **kwargs)
    # sanity check:
    if second_pass.hostname and second_pass.port:
        return second_pass
    # exhausted!
    raise ApputilsParseError(
        'Cannot determine hostname/port for given netlogger string: "{url}"'.format(url=url))


# TODO(s.finucane001@gmail.com): replace/improve the ``safe name`` function paradigm!!!

def _make_safe_name(name):
    return "_".join(name.split()).replace('-', '_')


def _make_option_name(name):
    return name.lower().replace('_', '-')


class ArgumentParser(object):
    """
    """
    def __init__(self, prog_name='', prog_description='', prog_epilogue='',
                 prog_version=''):
        self._arg_parser = argparse.ArgumentParser(
            prog=prog_name, description=prog_description,
            epilog=prog_epilogue,
            fromfile_prefix_chars='@')

        #self.prog_version = prog_version

    @property
    def prog_version(self, value):
        self._arg_parser.add_argument(
            '--version', action='version',
            version='%(prog)s {vers}'.format(vers=value))

    def parse_args(self, args):
        return self._arg_parser.parse_args(args=args)

    def add_argument(self, name, help_='', type_=str, nargs=1):
        safe_name = _make_safe_name(name)
        self._arg_parser.add_argument(
            safe_name, metavar=safe_name.upper(), type=type_, nargs=nargs,
            help=help_)

    def add_restricted_argument(self, name, choices, help_='', type_=str, nargs=1):
        safe_name = _make_safe_name(name)

        augmented_help = '{orig} (choices: {c})'.format(orig=help_,
                                                        c=str(choices).strip().replace('[', '').replace(']', ''))

        self._arg_parser.add_argument(
            safe_name, metavar=safe_name.upper(), type=type_, nargs=nargs,
            choices=choices,
            help=augmented_help)

    def add_option(self, name, unix_flag=None, default=None, help_='',
                   type_=str, dest=None):

        safe_name = _make_safe_name(name)
        if dest is None:
            dest = safe_name

        optname = _make_option_name(safe_name)
        if unix_flag is not None:
            self._arg_parser.add_argument(
                '-{f}'.format(f=unix_flag),
                '--{n}'.format(n=optname), dest=dest, action='append',
                default=[default], type=type_,
                help=help_)
        else:
            self._arg_parser.add_argument(
                '--{n}'.format(n=optname), dest=dest, action='append',
                default=[default], type=type_,
                help=help_)

    def add_restricted_option(self, name, choices, unix_flag=None, default=None, help_='', type_=str, dest=None):
        if default is None:
            default = choices[0]

        safe_name = _make_safe_name(name)
        if dest is None:
            dest = safe_name

        optname = _make_option_name(safe_name)
        if unix_flag is not None:
            self._arg_parser.add_argument(
                '-{f}'.format(f=unix_flag),
                '--{n}'.format(n=optname), dest=dest, action='append',
                choices=choices,
                default=default, type=type_,
                help=help_)
        else:
            self._arg_parser.add_argument(
                '--{n}'.format(n=optname), dest=dest, action='append',
                choices=choices,
                default=default, type=type_,
                help=help_)

    def add_counted_option(self, name, unix_flag=None, default=None, help_='', dest=None):
        if default is None:
            default = 0

        safe_name = _make_safe_name(name)
        if dest is None:
            dest = safe_name

        optname = _make_option_name(safe_name)
        if unix_flag is not None:
            self._arg_parser.add_argument(
                '-{f}'.format(f=unix_flag),
                '--{n}'.format(n=optname), dest=dest, action='count',
                default=default,
                help=help_)
        else:
            self._arg_parser.add_argument(
                '--{n}'.format(n=optname), dest=dest, action='count',
                default=default,
                help=help_)

    def add_switch(self, name, unix_flag=None, default=None, help_='', dest=None):
        action = 'store_true'
        if default:
            action = 'store_false'

        safe_name = _make_safe_name(name)
        if dest is None:
            dest = safe_name

        optname = _make_option_name(safe_name)
        if unix_flag is not None:
            self._arg_parser.add_argument(
                '-{f}'.format(f=unix_flag),
                '--{n}'.format(n=optname), dest=dest, action=action,
                help=help_)
        else:
            self._arg_parser.add_argument(
                '--{n}'.format(n=optname), dest=dest, action=action,
                help=help_)
