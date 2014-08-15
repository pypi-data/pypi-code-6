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

import os

from ._ConfirmAction import ConfirmAction
from ..util import AbortError, ConfigError, ui_print


class WriteAction(ConfirmAction):
    """An Action that returns the line with possible colouring"""

    instances = dict()

    def __init__(self, cfg, ui_confirm):
        self.mode = 'w' if cfg.get('truncate', False) else 'a'

        if 'filename' in cfg:
            filename = cfg['filename']
            if filename.startswith('~'):
                filename = os.path.expanduser(filename)
            self.filename = os.path.abspath(filename)

        super(WriteAction, self).__init__(cfg, ui_confirm, ['filename'])

        WriteAction.open_file_instance(self)

    @classmethod
    def open_file_instance(cls, inst):
        try:
            file_instances = cls.instances[inst.filename]
        except KeyError:
            file_instances = list()
            cls.instances[inst.filename] = file_instances

        if file_instances:
            inst.fp = file_instances[0]

            if inst.fp.mode != inst.mode:
                raise ConfigError('File {} is opened in conflicting modes.'.format(inst.filename))
        else:
            try:
                inst.fp = open(inst.filename, inst.mode)
            except (OSError, IOError) as err:
                ui_print().error(
                    'Cannot open {} for writing.'.format(inst.filename),
                    str(err), sep='\n'
                )
                raise AbortError()

        file_instances.append(inst)

    @classmethod
    def close_file_instance(cls, inst):
        try:
            file_instances = cls.instances[inst.filename]
        except KeyError:
            return

        try:
            file_instances.remove(inst)
        except ValueError:
            pass

        if not file_instances:
            inst.fp.close()

    def run_on(self, line):
        self.fp.write(line)
        self.fp.flush()
        os.fsync(self.fp)
        return None

    def release_resources(self):
        WriteAction.close_file_instance(self)

    def confirm_message(self):
        return 'The file {} will be {}.'.format(
            self.filename,
            'overwritten' if self.mode == 'w' else 'written to',
        )
