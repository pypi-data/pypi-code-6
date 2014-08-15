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


def get_arg_group(argparser, mode_name):
    return argparser.add_argument_group('{} Mode Only'.format(mode_name))


def add_cmdln_argument(group, mode_name, *args, **kwargs):
    prefix = mode_name.lower()
    _args = map(list, args)

    for i in range(0, len(args)):
        if args[i][:2] == '--':
            _args[i] = '--{}-{}'.format(prefix, args[i][2:])
        elif args[i][0] == '-':
            _args[i] = '-{}-{}'.format(prefix, args[i][1:])
        else:
            raise ValueError('Mode arguments may not be positional')

    group.add_argument(*_args, **kwargs)
